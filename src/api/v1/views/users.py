#!/usr/bin/python3
"""This file contain views that define basic endpoints for working with
users. These include CRUD operations on the users table. Authentication is handled in a
separate file. See user_auth.py"""
from flask import jsonify, request
from werkzeug.security import generate_password_hash
from os import environ
from api.v1.views import api_views
from models.user import User
from flasgger.utils import swag_from
from utils.decorators import token_required

@api_views.get('/users', strict_slashes=False)
@swag_from('documentation/users/get_users.yml', methods=['GET'])
@token_required
def get_users(email=None):
    """Retrieve all user from the database"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@api_views.get('/users/me', strict_slashes=False)
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
    user = User.query.get(id)
    try:
        return jsonify(user.to_dict()), 200
    except AttributeError:
        return jsonify({'error': 'Not Found'}), 404
    
@api_views.put('/users/me', strict_slashes=False)
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
        user.age = data.get('age', user.age)
        user.save()
        return jsonify(user.to_dict()), 200
    except AttributeError:
        return jsonify({'error': 'Not Found'}), 404
    except Exception as e:
        return jsonify({'error': 'Not a JSON'}), 400
    
@api_views.put('/users/me/change_password', strict_slashes=False)
@swag_from('documentation/users/change_password.yml', methods=['PUT'])
@token_required
def change_password(email):
    """Change, not reset password"""
    user = User.get_user_by_email(email)
    try:
        data = request.get_json()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        if user.password == generate_password_hash(old_password):
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
