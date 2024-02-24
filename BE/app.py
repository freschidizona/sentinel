#region Imports
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mqtt import Mqtt
from os import environ
import json

#endregion

#region Flask, SQLAlchemy
app = Flask(__name__)
CORS(app) # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
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
   create_log(payload)
#endregion

#region Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def json(self):
        return { 'id' : self.id, 'name' : self.name }

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    col = db.Column(db.Integer, unique=False, nullable=False)
    strength = db.Column(db.Float, unique=False, nullable=False)
    bpm = db.Column(db.Integer, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def json(self):
        return { 'id' : self.id, 'id_user' : self.id_user, 'col' : self.col, 'strength' : self.strength, 'created_on' : self.created_on, 'updated_on' : self.updated_on }

class Request(db.Model):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def json(self):
        return { 'id' : self.id, 'name' : self.name, 'created_on' : self.created_on, 'updated_on' : self.updated_on }

db.create_all()
#endregion

#region Routes
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

        print(latest_logs)

        return jsonify(latest_logs), 200
    except Exception as e:
        return make_response(jsonify({'message' : 'Error getting all Logs : ', 'error' : str(e)}), 500)
#endregion
    
#region Utils
def create_log(log = None):
    data = log if log else request.get_json(force=True)
    # !!!
    new_log = Log(id_user = data['idOp'], col = (data['col'] / 10), strength = data['strength'], bpm = data['BPM']) # Create new user using User model
    db.session.add(new_log) # Add new user using SQLAlchemy
    db.session.commit() # Commit this session
#endregion


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

