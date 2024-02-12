#region Imports
from app import app, socketio
from app import db, User, Log, Request

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from os import environ
#endregion

@app.route('/api/flask/users', methods=['POST']) # Create a new User
def create_user():
    try:
        data = request.get_json() # Get data from request
        new_user = User(name = data['name'], email = data['email'], job = data['job']) # Create new user using User model
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
    
@app.route('/api/flask/users/<id>', methods=['GET']) # Get all Users
def get_user(id):
    try:
        user = User.query.filter_by(id = id).first() # Get User by its ID
        if user:
            return make_response(jsonify({'user' : user.json()}), 200)
        return make_response(jsonify({'message' : 'User not found!'}), 404)
    except Exception as e:
        return make_response(jsonify({'message' : 'Error creating new User : ', 'error' : str(e)}), 500)

@app.route('/api/flask/users/<id>', methods=['PUT']) # Get all Users
def update_user(id):
    try:
        user = User.query.filter_by(id = id).first() # Get User by its ID
        if user:
            data = request.get_json()
            user.name = data['name']
            db.session.commit()
            return make_response(jsonify({'message' : 'User updated!'}), 200)
        return make_response(jsonify({'message' : 'User not found!'}), 404)
    except Exception as e:
        return make_response(jsonify({'message' : 'Error creating new User : ', 'error' : str(e)}), 500)

@app.route('/api/flask/users/<id>', methods=['DELETE']) # Get all Users
def delete_user(id):
    try:
        user = User.query.filter_by(id = id).first() # Get User by its ID
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message' : 'User deleted!'}), 200)
        return make_response(jsonify({'message' : 'User not found!'}), 404)
    except Exception as e:
        return make_response(jsonify({'message' : 'Error creating new User : ', 'error' : str(e)}), 500)
    
@socketio.on('my event')
def log_message(message):
    emit('my response', {'data': 'got it!'})

# @socketio.on('get_users') # Get all Users
# def get_users():
#     try:
#         users = User.query.all() # Get all Users from table
#         users_data = [{ 'id' : user.id, 'name' : user.name } for user in users]
#         emit('my response', users, namespace='/users')
#     except Exception as e:
#         print('ERROR')
#         # return make_response(jsonify({'message' : 'Error getting all Users : ', 'error' : str(e)}), 500)