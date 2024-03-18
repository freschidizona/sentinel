#region Imports
from flask import Flask, request, jsonify, make_response, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_mqtt import Mqtt
from flask_socketio import SocketIO, emit
from flask_session import Session
from config import ApplicationConfig
from flask_sqlalchemy import SQLAlchemy
import datetime
from os import environ
import json
#endregion

#region Flask, SQLAlchemy, Bcrypt, Websockets
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object(ApplicationConfig)
server_session = Session(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins='*')

#region Database, Models
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(42), unique=False, nullable=False)
    surname = db.Column(db.String(42), unique=False, nullable=False)
    email = db.Column(db.String(42), unique=True, nullable=False)
    password = db.Column(db.String(96), unique=False, nullable=False)

    def json(self):
        return { 'id' : self.id, 
                'name' : self.name, 
                'surname' : self.surname, 
                'email' : self.email, 
                'password' : self.password }
    
class Anchor(db.Model):
    __tablename__ = 'anchors'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80), unique=True, nullable=False)
    index = db.Column(db.String(2), unique=False, nullable=True)
    status = db.Column(db.Integer, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def json(self):
        return { 'id' : self.id, 
                'address' : self.address,
                'index' : self.index, 
                'status' : self.status, 
                'created_on' : self.created_on, 
                'updated_on' : self.updated_on }

class Worker(db.Model):
    __tablename__ = 'workers'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(42), unique=False, nullable=True)
    surname = db.Column(db.String(42), unique=False, nullable=True)

    def json(self):
        return { 'id' : self.id, 
                'address' : self.address, 
                'name' : self.name, 
                'surname' : self.surname }

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    worker_addr = db.Column(db.String(80), unique=False, nullable=False)
    anchor_id = db.Column(db.String(80), unique=False, nullable=False)
    bpm = db.Column(db.Integer, unique=False, nullable=True)
    temp = db.Column(db.Integer, unique=False, nullable=True)
    chol = db.Column(db.Integer, unique=False, nullable=True)
    sug = db.Column(db.Integer, unique=False, nullable=True)
    type = db.Column(db.Integer, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def json(self):
        return { 'id' : self.id, 
                'worker_addr' : self.worker_addr, 
                'anchor_id' : self.anchor_id, 
                'bpm' : self.bpm, 
                'temp' : self.temp, 
                'chol' : self.chol, 
                'sug' : self.sug, 
                'type' : self.type, 
                'created_on' : self.created_on, 
                'updated_on' : self.updated_on }

db.create_all()

#endregion

#endregion

#region Utils
def mqtt_create_worker(address):
    try:
        worker = Worker.query.filter_by(address = address).first() # Get Worker by its ID
        if not worker:
            new_worker = Worker(address = address)
            db.session.add(new_worker)
            db.session.commit()
    except Exception as e:
        print(e)
def mqtt_create_anchor(address):
    try:
        print("[INFO] Check if Anchor exists: " + address)
        anchor = Anchor.query.filter_by(address = address).first() # Get Anchor by its ID
        if not anchor:
            new_anchor = Anchor(address = address, status = 0)
            db.session.add(new_anchor)
            db.session.commit()
    except Exception as e:
        print(e)
def mqtt_create_log(data):
    try:
        new_log = Log(
            worker_addr = data['worker_addr'], 
            anchor_id = data['anchor_id'], 
            type = data['type']) if data['type'] == 1 else Log(
                worker_addr = data['worker_addr'], 
                anchor_id = data['anchor_id'], 
                bpm = data['bpm'], 
                temp = data['temp'],
                chol = data['chol'], 
                sug = data['sug'], 
                type = data['type'])
        db.session.add(new_log)
        db.session.commit()

        # Emit new logs to clients
        if data['type'] == 1 or data['type'] == 5:
            # Emit notify if User requests help
            get_notify()
        else: get_latest_logs() # Emit new logs
    except Exception as e:
        print(e)
#endregion

#region MQTT
#region Config
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
topic = '/sentinel/messages'

mqtt_client = Mqtt(app)
#endregion
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    try:
        data = message.payload.decode()
        print("[MQTT] Received message on topic " + message.topic + " : " + data)
        payload=json.loads(data)
        
        # print("[INFO] Received JSON : " + format(payload))

        # Create new Worker if it doesn't exist
        mqtt_create_worker(str(payload.get('worker_addr')))
        # Create new Anchor if it doesn't exist
        mqtt_create_anchor(str(payload.get('anchor_id')))
        # Create new Log
        mqtt_create_log(payload)
    except Exception as e:
        print(e)
#endregion

#region Routes

#region SocketIO
@socketio.on('anchors')
def get_anchors():
    print('[EMIT] Emitting Anchors...')
    anchors = Anchor.query.all()
    anchor_data = [{ 
        'id' : anchor.id, 
        'address' : anchor.address, 
        'status' : anchor.status, 
        'created_on' : anchor.created_on.strftime('%Y-%m-%d %H:%M:%S'), 
        'updated_on' : anchor.updated_on.strftime('%Y-%m-%d %H:%M:%S') } for anchor in anchors]
    print(format(anchor_data))
    emit('anchorsEvent', {
        'data': anchor_data,
        'id': request.sid
    }, broadcast=True)

@socketio.on('latestLogs')
def get_latest_logs():
    print('[EMIT] Emitting Latest Logs...')
    # logs = Log.query\
    #     .join(Anchor, Log.anchor_id == Anchor.id)\
    #     .add_columns(Log, User.name)\
    #     .filter(User.id == Log.id_user)\
    #     .all()
    logs = Log.query.all()
    logs_data = [{ 
        'id' : log.id, 
        'worker_addr' : log.worker_addr, 
        'anchor_id' : log.anchor_id, 
        'bpm' : log.bpm, 
        'temp' : log.temp, 
        'chol' : log.chol, 
        'sug' : log.sug, 
        'created_on': log.created_on.strftime('%Y-%m-%d %H:%M:%S') } for log in logs]
    latest_logs_dict = {}
    for log in logs_data:
        worker_addr = log['worker_addr']
        if worker_addr not in latest_logs_dict or log['created_on'] > latest_logs_dict[worker_addr]['created_on']:
            latest_logs_dict[worker_addr] = log
    latest_logs = list(latest_logs_dict.values())

    print(format(latest_logs))
    emit('latestLogsEvent', {
        'data': latest_logs,
        'id': request.sid
    }, broadcast=True)

@socketio.on('notify')
def get_notify():
    try:
        print('[EMIT] Emitting Notify...')
        notify = Log.query.filter(Log.type == 1).all()
        notify_data = [{ 
            'id' : e.id, 
            'worker_addr' : e.worker_addr,
            'type' : e.type,
            'created_on': e.created_on.strftime('%Y-%m-%d %H:%M:%S') } for e in notify]
        emit('notifyEvent', {
            'data': notify_data,
            'id': request.sid
        }, broadcast=True)
    except Exception as e:
        print(e)
#endregion

#region User
@app.route('/api/register', methods=['POST']) # Create a new User
def register():
    try:
        data = request.get_json(force=True)
        admin = User(
            name = data['name'], 
            surname = data['surname'], 
            email = data['email'], 
            password = bcrypt.generate_password_hash(data['password']).decode("utf-8", "ignore"))
        db.session.add(admin)
        db.session.commit() # Commit this session

        session["user_id"] = admin.id
        return jsonify({ # Return the new obj itself to handle ID
            'id' : admin.id,
            'name' : admin.name,
            'surname' : admin.surname,
            'email' : admin.email
        }), 201 # HTTP Code
    except Exception as e:
        return make_response(jsonify({'message' : 'Error creating new Admin : ', 'error' : str(e)}), 500)

@app.route('/api/login', methods=['POST']) # Create a new User
def login():
    try:
        data = request.get_json(force=True)

        admin = User.query.filter_by(email=data['email']).first()

        if admin is None:
            return jsonify({"error": "Admin do not found in DB"}), 401
        if not bcrypt.check_password_hash(admin.password, data['password']):
            return jsonify({"error": "Error, wrong password"}), 401
        
        session["user_id"] = admin.id
        return jsonify({
            "id": admin.id,
            "email": admin.email
        })
    except Exception as e:
        return make_response(jsonify({'message' : 'Error while logging : ', 'error' : str(e)}), 500)

@app.route("/api/logout", methods=["POST"])
def logout_user():
    try:
        session.pop("user_id")
        return "200"
    except Exception as e:
        return make_response(jsonify({'message' : 'Error while logging out : ', 'error' : str(e)}), 500)

@app.route("/api/@me", methods=["GET"])
def get_current_user():
    try:
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        
        user = User.query.filter_by(id=user_id).first()
        return jsonify({
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "email": user.email
        })
    except Exception as e:
            return make_response(jsonify({'message' : 'Error while getting current Admin : ', 'error' : str(e)}), 500)
#endregion

#region Users
# Non più utilizzate, si rifanno al model Worker. Modifica User con Worker
@app.route('/api/users', methods=['POST']) # Create a new User
def create_user():
    try:
        data = request.get_json(force=True) # Get data from request
        new_user = User(name = data['name']) # Create new user using User model
        db.session.add(new_user) # Add new user using SQLAlchemy
        db.session.commit() # Commit this session

        return jsonify({ # Return the new obj itself to handle ID
            'id' : new_user.id,
            'name' : new_user.name
        }), 201 # HTTP Code
    except Exception as e:
        return make_response(jsonify({'message' : 'Error creating new User : ', 'error' : str(e)}), 500)

@app.route('/api/users', methods=['GET']) # Get all Users
def get_users():
    try:
        users = User.query.all() # Get all Users from table
        users_data = [{ 'id' : user.id, 'name' : user.name } for user in users]
        return jsonify(users_data), 200
    except Exception as e:
        return make_response(jsonify({'message' : 'Error getting all Users : ', 'error' : str(e)}), 500)
#endregion

#region Anchors
@app.route('/api/anchors', methods=['POST'])
def create_anchor():
    try:
        # Get data from request
        data = request.get_json(force=True)
        # Create new anchor using Anchor model
        new_anchor = Anchor(address = data['address'], status = data['status'])
        db.session.add(new_anchor)
        db.session.commit()
        # Emit anchors to all clients 
        get_anchors()
        # Return the new obj itself
        return jsonify(data), 201
    except Exception as e:
        return make_response(jsonify({'message' : 'Error creating new Anchor : ', 'error' : str(e)}), 500)

@app.route('/api/anchors/<address>', methods=['PUT'])
def ping_anchor(address):
    try:
        # anchors = Anchor.query.all()
        # anchor_data = [{ 
        #     'id' : anchor.id, 
        #     'address' : anchor.address, 
        #     'status' : anchor.status ,
        #     'created_on' : anchor.created_on, 
        #     'updated_on' : anchor.updated_on } for anchor in anchors]
        
        # Set anchors status to 1 if updated at is greater than 1 hour

        anchor = Anchor.query.filter_by(address = address).first()
        if anchor:
            anchor.created_on = datetime.datetime.now()
            db.session.commit()
            return make_response(jsonify({'message' : 'Anchor updated!'}), 200)
        return make_response(jsonify({'message' : 'Anchor not found!'}), 404)
    except Exception as e:
        return make_response(jsonify({'message' : 'Error : ', 'error' : str(e)}), 500)
#endregion

@app.route('/api/ack', methods=['POST']) 
def send_ack():
    try:
        data = request.get_json(force=True)
        msg = json.dumps(data)
        print("[ACK] Sending ACK : " + data["worker_addr"])
        mqtt_client.publish("/sentinel/ack", msg)
        return jsonify(data), 201
    except Exception as e:
        return make_response(jsonify({'message' : 'Error sending ACK : ', 'error' : str(e)}), 500)

@app.route('/api/logs', methods=['POST']) 
def create_log():
    try:
        data = request.get_json(force=True)
        new_log = Log(
            id_user = data['id_user'], 
            col = data['col'], 
            strength = data['strength'], 
            bpm = data['bpm'], 
            temp = data['temp'], 
            type = data['type'])
        db.session.add(new_log)
        db.session.commit()

        return jsonify(data), 201
    except Exception as e:
        return make_response(jsonify({'message' : 'Error creating new Log : ', 'error' : str(e)}), 500)

@app.route('/api/logs', methods=['GET'])
def get_logs():
    try:
        logs = Log.query.all()
        logs_data = [{ 'id' : log.id, 'id_user' : log.id_user, 'col' : log.col, 'strength' : log.strength, 'bpm' : log.bpm } for log in logs]

        return jsonify(logs_data), 200
    except Exception as e:
        return make_response(jsonify({'message' : 'Error getting all Logs : ', 'error' : str(e)}), 500) 

# @app.route('/api/latest_logs', methods=['GET']) # Get all Users
# def get_latest_logs():
#     try:
#         logs = Log.query.all()
#         logs_data = [{ 'id' : log.id, 'id_user' : log.id_user, 'col' : log.col, 'strength' : log.strength, 'bpm' : log.bpm, 'created_on': log.created_on } for log in logs]

#         latest_logs_dict = {}
#         for log in logs_data:
#             id_user = log['id_user']
#             if id_user not in latest_logs_dict or log['created_on'] > latest_logs_dict[id_user]['created_on']:
#                 latest_logs_dict[id_user] = log
#         latest_logs = list(latest_logs_dict.values())

#         print(format(latest_logs))

#         return jsonify(latest_logs), 200
#     except Exception as e:
#         return make_response(jsonify({'message' : 'Error getting all Logs : ', 'error' : str(e)}), 500)
#endregion


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=4000)
    socketio.run(app, host='0.0.0.0', port=4000)

