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
def _create_user(id):
    try:
        user = User.query.filter_by(id = id).first() # Get User by its ID
        if not user:
            new_user = User(id = id) # Create new user using User model
            db.session.add(new_user) # Add new user using SQLAlchemy
            db.session.commit()
    except Exception as e:
        return
def create_log(data):
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

   # print('Received message on topic:' + message.topic + ' with payload: ' + data)
   
   # _create_user(str(payload.get('user_addr')))
   # create_log(payload)
#endregion

#region Routes

#region WS
@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)
    emit('my response', data, broadcast=True) # my response is event name for UI

@socketio.on('connect')
def connect():
    print('Someone connected to websocket!')
    print('Client connected: ' + request.sid)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected: ' + request.sid)

@socketio.on('handle_message')
def connect(data):
    print('Data from client: ' + str(data))
    emit('data', {
        'data': data,
        'id': request.sid
    }, broadcast=True)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

@socketio.on('my_event')
def handle_my_custom_event(arg1, arg2, arg3):
    print('received args: ' + arg1 + arg2 + arg3)
#endregion

#region Admins
@app.route('/api/flask/register', methods=['POST']) # Create a new User
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

@app.route('/api/flask/login', methods=['POST']) # Create a new User
def login():
    try:
        data = request.get_json(force=True)
        print(format(data))

        admin = Admin.query.filter_by(email=data['email']).first()

        if admin is None:
            return jsonify({"error": "Unauthorized"}), 401
        if not bcrypt.check_password_hash(admin.password, data['password']):
            return jsonify({"error": "Unauthorized"}), 401
        
        session["user_id"] = admin.id
        return jsonify({
            "id": admin.id,
            "email": admin.email
        })
    except Exception as e:
        return make_response(jsonify({'message' : 'Error while logging : ', 'error' : str(e)}), 500)

@app.route("/api/flask/logout", methods=["POST"])
def logout_user():
    try:
        session.pop("user_id")
        return "200"
    except Exception as e:
        return make_response(jsonify({'message' : 'Error while logging out : ', 'error' : str(e)}), 500)

@app.route("/api/flask/@me", methods=["GET"])
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
@app.route('/api/flask/users', methods=['POST']) # Create a new User
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

@app.route('/api/flask/users', methods=['GET']) # Get all Users
def get_users():
    try:
        users = User.query.all() # Get all Users from table
        users_data = [{ 'id' : user.id, 'name' : user.name } for user in users]
        return jsonify(users_data), 200
    except Exception as e:
        return make_response(jsonify({'message' : 'Error getting all Users : ', 'error' : str(e)}), 500)
#endregion

#region Anchors
@app.route('/api/flask/anchors', methods=['POST'])
def create_anchor():
    try:
        data = request.get_json(force=True)
        new_anchor = Anchor(address = data['address'], status = data['status'])
        db.session.add(new_anchor)
        db.session.commit()

        return jsonify(data), 201
    except Exception as e:
        return make_response(jsonify({'message' : 'Error creating new Anchor : ', 'error' : str(e)}), 500)

@app.route('/api/flask/anchors/<address>', methods=['PUT'])
def ping_anchor(address):
    try:
        anchor = Anchor.query.filter_by(address = address).first()
        if anchor:
            anchor.created_on = datetime.datetime.now()
            db.session.commit()
            return make_response(jsonify({'message' : 'Anchor updated!'}), 200)
        return make_response(jsonify({'message' : 'Anchor not found!'}), 404)
    except Exception as e:
        return make_response(jsonify({'message' : 'Error : ', 'error' : str(e)}), 500)

# Trigger to set Anchor's state equals to 1 if updated_on < datetime.now() - 1h | DA RIVEDERE
def update_anchor_state():
    try:
        update_anchor_state = DDL('''\
            CREATE TRIGGER update_anchor_state UPDATE OF updated_on ON anchors
            BEGIN
                UPDATE anchors SET status = 1 WHERE (updated_on < datetime('now', '-1 hour'));
            END;''')
        event.listen(Anchor.__table__, 'after_create', update_anchor_state)
        db.session.commit()
    except Exception as e:
        return make_response(jsonify({'message' : 'Error : ', 'error' : str(e)}), 500)

@app.route('/api/flask/anchors', methods=['GET'])
def get_anchors():
    try:
        anchors = Anchor.query.all()
        anchor_data = [{ 'id' : anchor.id, 'address' : anchor.address, 'status' : anchor.status, 'created_on' : anchor.created_on, 'updated_on' : anchor.updated_on } for anchor in anchors]
        return jsonify(anchor_data), 200
    except Exception as e:
        return make_response(jsonify({'message' : 'Error getting all Anchors : ', 'error' : str(e)}), 500)
    
# scheduler.every(1).hour.do(update_anchor_state.execute)
#endregion


@app.route('/api/flask/logs', methods=['POST']) 
def _create_log():
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

@app.route('/api/flask/logs', methods=['GET'])
def get_logs():
    try:
        logs = Log.query.all()
        logs_data = [{ 'id' : log.id, 'id_user' : log.id_user, 'col' : log.col, 'strength' : log.strength, 'bpm' : log.bpm } for log in logs]

        return jsonify(logs_data), 200
    except Exception as e:
        return make_response(jsonify({'message' : 'Error getting all Logs : ', 'error' : str(e)}), 500) 
@app.route('/api/flask/latest_logs', methods=['GET']) # Get all Users
def get_latest_logs():
    try:
        logs = Log.query.all()
        logs_data = [{ 'id' : log.id, 'id_user' : log.id_user, 'col' : log.col, 'strength' : log.strength, 'bpm' : log.bpm, 'created_on': log.created_on } for log in logs]

        latest_logs_dict = {}
        for log in logs_data:
            id_user = log['id_user']
            if id_user not in latest_logs_dict or log['created_on'] > latest_logs_dict[id_user]['created_on']:
                latest_logs_dict[id_user] = log
        latest_logs = list(latest_logs_dict.values())

        # print(latest_logs)

        return jsonify(latest_logs), 200
    except Exception as e:
        return make_response(jsonify({'message' : 'Error getting all Logs : ', 'error' : str(e)}), 500)
#endregion


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=4000)
    socketio.run(app, host='0.0.0.0', port=4000)

