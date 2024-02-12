#region Imports
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mqtt import Mqtt
from flask_socketio import SocketIO, emit
from os import environ
from engineio.async_drivers import gevent, eventlet
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
   data = dict(
       topic=message.topic,
       payload=message.payload.decode()
  )
   print('Received message on topic: {topic} with payload: {payload}'.format(**data))
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

socketio = SocketIO(app, 
                    host='0.0.0.0', 
                    debug=True, 
                    port=4000,
                    cors_allowed_origins='*', 
                    async_mode='gevent',
                    use_reloader=True)

@socketio.on('connect')
def test_connect(auth):
    emit('my response', {'data': 'Connected'})

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

@app.route('/api/flask/users', methods=['GET']) # Get all Users
def get_users():
    try:
        users = User.query.all() # Get all Users from table
        users_data = [{ 'id' : user.id, 'name' : user.name } for user in users]
        return jsonify(users_data), 200
    except Exception as e:
        return make_response(jsonify({'message' : 'Error getting all Users : ', 'error' : str(e)}), 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
    socketio.run(app)

