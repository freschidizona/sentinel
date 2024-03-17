#region Imports
from flask import Flask, request, jsonify, make_response, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_mqtt import Mqtt
from flask_socketio import SocketIO, emit
from flask_session import Session
from config import ApplicationConfig
from models import db, Admin, User, Log, Anchor
from sqlalchemy import event, DDL
import datetime
from os import environ
import json
#endregion

#region Flask, SQLAlchemy, Bcrypt, Websockets
app = Flask(__name__)

bcrypt = Bcrypt(app)
app.config.from_object(ApplicationConfig)
db.init_app(app)
with app.app_context():
    db.create_all()
server_session = Session(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins='*')
#endregion

#region Utils
def mqtt_create_user(id):
    try:
        user = User.query.filter_by(id = id).first() # Get User by its ID
        if not user:
            new_user = User(id = id) # Create new user using User model
            db.session.add(new_user) # Add new user using SQLAlchemy
            db.session.commit()
    except Exception as e:
        return
def mqtt_create_log(data):
    new_log = Log(id_user = data['user_addr'], col = data['col'], strength = data['rssi'], bpm = data['bpm'], temp = data['temp'], type = data['type']) # Create new user using User model
    db.session.add(new_log) # Add new log using SQLAlchemy
    db.session.commit() # Commit this session
#endregion

#region MQTT
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
topic = '/sentinel/logs'

mqtt_client = Mqtt(app)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    data = message.payload.decode()
    data = data.replace("(", "").replace(")", "")

    payload=json.loads(data)

    # mqtt_create_user(str(payload.get('user_addr')))
    mqtt_create_log(payload)
#endregion

#region Routes

#region SocketIO
@socketio.on('anchors')
def get_anchors():
    print('[INFO] Emitting Anchors...')
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
    print('[INFO] Emitting Latest Logs...')
    logs = Log.query\
        .join(User, Log.id_user == User.id)\
        .add_columns(Log, User.name)\
        .filter(User.id == Log.id_user)\
        .all()
    logs_data = [{ 
        'id' : log.id, 
        'address' : log.name, 
        'col' : log.col, 
        'strength' : log.strength, 
        'bpm' : log.bpm, 
        'created_on': log.created_on.strftime('%Y-%m-%d %H:%M:%S') } for log in logs]
    latest_logs_dict = {}
    for log in logs_data:
        id_user = log['id_user']
        if id_user not in latest_logs_dict or log['created_on'] > latest_logs_dict[id_user]['created_on']:
            latest_logs_dict[id_user] = log
    latest_logs = list(latest_logs_dict.values())

    print(format(latest_logs))
    emit('latestLogsEvent', {
        'data': latest_logs,
        'id': request.sid
    }, broadcast=True)

# @socketio.on('notify')
# def get_notify():
#     print('[INFO] Emitting Notify...')
#     notify = Log.query.filter(Log.type == 2 or Log.type == 5).all()
#     notify_data = [{ 
#         'id' : notify.id, 
#         'address' : notify.name, 
#         'col' : notify.col, 
#         'strength' : notify.strength, 
#         'bpm' : notify.bpm, 
#         'created_on': notify.created_on.strftime('%Y-%m-%d %H:%M:%S') } for notify in notify_data]
#     print(format(notify_data))
#     emit('notifyEvent', {
#         'data': notify_data,
#         'id': request.sid
#     }, broadcast=True)
#endregion

#region Admins
@app.route('/api/register', methods=['POST']) # Create a new User
def register():
    try:
        data = request.get_json(force=True)
        print(format(data))
        admin = Admin(
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
        print(format(data))

        admin = Admin.query.filter_by(email=data['email']).first()

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
        
        user = Admin.query.filter_by(id=user_id).first()
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

