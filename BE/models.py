from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(42), unique=False, nullable=False)
    surname = db.Column(db.String(42), unique=False, nullable=False)
    email = db.Column(db.String(42), unique=True, nullable=False)
    password = db.Column(db.String(96), unique=False, nullable=False)

    def json(self):
        return { 'id' : self.id, 'name' : self.name, 'surname' : self.surname, 'email' : self.email, 'password' : self.password }
    
class Anchor(db.Model):
    __tablename__ = 'anchors'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.Integer, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def json(self):
        return { 'id' : self.id, 'address' : self.address, 'status' : self.status, 'created_on' : self.created_on, 'updated_on' : self.updated_on }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=True)

    def json(self):
        return { 'id' : self.id, 'name' : self.name }

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    col = db.Column(db.Integer, unique=False, nullable=False)
    strength = db.Column(db.Float, unique=False, nullable=False)
    bpm = db.Column(db.Integer, unique=False, nullable=False)
    temp = db.Column(db.Integer, unique=False, nullable=False)
    type = db.Column(db.Integer, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def json(self):
        return { 'id' : self.id, 'id_user' : self.id_user, 'col' : self.col, 'strength' : self.strength, 'created_on' : self.created_on, 'updated_on' : self.updated_on }