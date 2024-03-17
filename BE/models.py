from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    index = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.Integer, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def json(self):
        return { 'id' : self.id, 
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
    anchor_id = db.Column(db.Integer, unique=False, nullable=False)
    bpm = db.Column(db.Integer, unique=False, nullable=False)
    temp = db.Column(db.Integer, unique=False, nullable=False)
    chol = db.Column(db.Integer, unique=False, nullable=False)
    sug = db.Column(db.Integer, unique=False, nullable=False)
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