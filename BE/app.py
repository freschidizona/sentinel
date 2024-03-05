#region Imports
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_mqtt import Mqtt
from os import environ
import json

#endregion

#region Flask, SQLAlchemy
app = Flask(__name__)
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
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

   print('Received message on topic:' + message.topic + ' with payload: ' + data)
   
   _create_user(str(payload.get('user_addr')))
   create_log(payload)
#endregion

#region Models
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(42), unique=False, nullable=False)
    surname = db.Column(db.String(42), unique=False, nullable=False)
    email = db.Column(db.String(42), unique=True, nullable=False)
    password = db.Column(db.String(96), unique=False, nullable=False)

    def json(self):
        return { 'id' : self.id, 'name' : self.name, 'surname' : self.surname, 'email' : self.email, 'password' : self.password }
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=True)

    def json(self):
        return { 'id' : self.id, 'name' : self.name }

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.String(80), db.ForeignKey('users.id'))
    col = db.Column(db.Integer, unique=False, nullable=False)
    strength = db.Column(db.Float, unique=False, nullable=False)
    bpm = db.Column(db.Integer, unique=False, nullable=False)
    temp = db.Column(db.Integer, unique=False, nullable=False)
    type = db.Column(db.Integer, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def json(self):
        return { 'id' : self.id, 'id_user' : self.id_user, 'col' : self.col, 'strength' : self.strength, 'created_on' : self.created_on, 'updated_on' : self.updated_on }

db.create_all()
#endregion

#region Routes

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
        
        # session["user_id"] = user.id
        return jsonify({
            "id": admin.id,
            "email": admin.email
        })
    except Exception as e:
        return make_response(jsonify({'message' : 'Error while logging : ', 'error' : str(e)}), 500)
#endregion



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

@app.route('/api/flask/logs', methods=['GET']) # Get all Users
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
    app.run(host='0.0.0.0', port=4000)

