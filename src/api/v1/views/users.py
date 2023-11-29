#!/usr/bin/python3
"""This file contain views that define basic endpoints for working with
users. These include authentication, and CRUD operations on the users table"""
from flask import jsonify, request, redirect, make_response
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from os import environ
from api.v1.views import api_views
from datetime import timedelta, datetime
from models.user import User
from flasgger.utils import swag_from
from .decorators import token_required

SECRET_KEY = environ.get("SECRET_KEY")

@api_views.post('/login', strict_slashes=False)
@swag_from('documentation/users/login.yml', methods=['POST'])
def login():
    """Authenticate a user if they already have an account"""
    try:
        auth = request.get_json()
        if not auth or not auth.get('email') or not auth.get('password'):
            return jsonify({'error': 'You must provide email and password'}), 400
        user = User.get_user_by_email(auth.get('email'))
        if not user:
            # user does not exist in the database
            return({'error': 'email doesnot exist'}), 400
        if check_password_hash(user.password, auth.get('password')):
            # information is valid and user exists
            token = jwt.encode({'email': auth.get('email'), 'exp': datetime.utcnow() + timedelta(hours=24)}, SECRET_KEY)
            response = make_response(jsonify(
                {'token': token, 'redirectUrl': 'http://0.0.0.0:5001/home'}
                ), 200)
            return response
        else:
            return jsonify({'error': 'Invalid password'}), 400
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

@api_views.post('/register', strict_slashes=False)
@swag_from('documentation/users/register.yml', methods=['POST'])
def register():
    """Create a new user"""
    try:
        user_data = request.get_json()
        email = user_data['email']
        password = user_data['password']
        first_name = user_data['first_name']
        last_name = user_data['last_name']
        country = user_data.get('country')
        age = user_data.get('age')
        title = user_data.get('title')
        phone = user_data.get('phone')
        new_user = User(email=email, password=password, first_name=first_name,
                        last_name=last_name, country=country, age=age, title=title, phone=phone)
        new_user.save()
        return jsonify({'id': new_user.id}), 201
    except KeyError:
        return jsonify({'error': 'Missing some data'}), 400
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

@api_views.get('/users', strict_slashes=False)
@swag_from('documentation/users/get_users.yml', methods=['GET'])
@token_required
def get_users(email=None):
    """Retrieve all user from the database"""
    users = User.all(User)
    return jsonify([user.to_dict() for user in users]), 200

@api_views.get('/users/myself', strict_slashes=False)
@swag_from('documentation/users/get_myself.yml', methods=['GET'])
@token_required
def get_myself(email=None):
    if email:
        user = User.get_user_by_email(email)
        return jsonify(user.to_dict()), 200

@api_views.get('/users/<string:id>', strict_slashes=False)
@swag_from('documentation/users/get_user.yml', methods=['GET'])
@token_required
def get_user(email, id):
    """Get a user by id"""
    user = User.get(User, id)
    try:
        return jsonify(user.to_dict()), 200
    except AttributeError:
        return jsonify({'error': 'Not Found'}), 404
    
@api_views.put('/users/myself', strict_slashes=False)
@swag_from('documentation/users/update_user.yml', methods=['PUT'])
@token_required
def update_myself(email):
    """Make changes to information stored under the same user"""
    user = User.get_user_by_email(email)
    try:
        data = request.get_json()
        user.title = data.get('title', user.title)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.country = data.get('country', user.country)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        user.save()
        User.reload()
        return jsonify(user.to_dict()), 200
    except AttributeError:
        return jsonify({'error': 'Not Found'}), 404
    except Exception as e:
        return jsonify({'error': 'Not a JSON'}), 400
    
@api_views.put('/users/myself/change_password', strict_slashes=False)
@swag_from('documentation/users/change_password.yml', methods=['PUT'])
@token_required
def change_password(email):
    """Change, not reset password"""
    user = User.get_user_by_email(email)
    try:
        data = request.get_json()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        if user.password == old_password:
            # The user does know the old password
            user.__setattr__('password', new_password)
            user.save()
            return jsonify({}), 200
        else:
            return jsonify({'error': 'Invalid Password'}), 403
    except AttributeError:
        return jsonify({'error': 'Not Found'}), 404
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

@api_views.put('/users/myself/reset_password', strict_slashes=False)
@swag_from('documentation/users/reset_password.yml', methods=['PUT'])
@token_required
def reset_password(email):
    """Reset password"""
    user = User.get_user_by_email(email)
    try:
        new_password = request.get_json().get('new_password')
        user.__setattr__('password', new_password)
        user.save()
        return jsonify({}), 200
    except AttributeError:
        return jsonify({'error': 'Not Found'}), 404
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

@api_views.delete('/users/myself', strict_slashes=False)
@token_required
def delete_user(email):
    """Delete a user's account"""
    user = User.get_user_by_email(email)
    try:
        user.delete()
        return jsonify({}), 204
    except AttributeError:
        return jsonify({'error': 'Not Found'}), 404