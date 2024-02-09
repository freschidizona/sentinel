from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mqtt import Mqtt
from os import environ

app = Flask(__name__)
CORS(app) # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# MQTT
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

TOPIC = 'sentinel/logs'
mqtt = Mqtt(app)

mqtt.subscribe(TOPIC)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
       print('Connected successfully')
       mqtt.subscribe(TOPIC) # subscribe topic
    else:
       print('Bad connection. Code:', rc)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print('Received message on topic: {topic} with payload: {payload}'.format(**data))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)

    def json(self):
        return { 'id' : self.id, 'name' : self.name }

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    col = db.Column(db.Integer, unique=False, nullable=False)
    strength = db.Column(db.Integer, unique=False, nullable=False)
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

import user_routes #, BE.log_routes as log_routes, BE.request_routes as request_routes