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
from utils.helpers import avoid_danger_in_json
from utils.logger import logger

@api_views.get('/users', strict_slashes=False)
@swag_from('documentation/users/get_users.yml', methods=['GET'])
@token_required
def get_users(email=None):
    """Retrieve all user from the database"""
    try:
        page = request.args.get('page', 0, type=int)
        limit = 20
        offset = page * limit
        users = User.query.offset(offset).limit(limit).all()
        response = jsonify([user.to_dict() for user in users]), 200
        logger.info(f'{len(users)} users retrieved successfully')
        return response
    except ValueError as e:
        logger.exception(e)
        return jsonify({'error': 'Invalid page number'}), 400
    except Exception as e:
        logger.exception(e)
        return jsonify({'error': 'Not Found'}), 404

@api_views.get('/users/me', strict_slashes=False)
@swag_from('documentation/users/get_myself.yml', methods=['GET'])
@token_required
def get_myself(email=None):
    try:
        if email:
            user = User.get_user_by_email(email)
            response = jsonify(user.to_dict()), 200
            logger.info(f'User {user.id} retrieved successfully')
            return response
    except AttributeError as e:
        logger.exception(e)
        return jsonify({'error': 'Not Found'}), 404

@api_views.get('/users/<string:id>', strict_slashes=False)
@swag_from('documentation/users/get_user.yml', methods=['GET'])
@token_required
def get_user(email, id):
    """Get a user by id"""
    try:
        user = User.query.get(id)
        response = jsonify(user.to_dict()), 200
        logger.info(f'User {user.id}retrieved successfully')
        return response
    except AttributeError as e:
        logger.exception(e)
        return jsonify({'error': 'not found'}), 404
    
@api_views.put('/users/me', strict_slashes=False)
@swag_from('documentation/users/update_user.yml', methods=['PUT'])
@token_required
def update_myself(email):
    """Make changes to information stored under the same user"""
    try:
        user = User.get_user_by_email(email)
        data = avoid_danger_in_json(**request.get_json())
        user.title = data.get('title', user.title)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.country = data.get('country', user.country)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        user.age = data.get('age', user.age)
        user.save()
        logger.info(f'User {user.id} updated successfully')
        return jsonify(user.to_dict()), 200
    except AttributeError as e:
        logger.exception(e)
        return jsonify({'error': 'not found'}), 404
    except Exception as e:
        logger.exception(e)
        return jsonify({'error': 'not a JSON'}), 400
    
@api_views.put('/users/me/change_password', strict_slashes=False)
@swag_from('documentation/users/change_password.yml', methods=['PUT'])
@token_required
def change_password(email):
    """Change, not reset password"""
    try:
        user = User.get_user_by_email(email)
        data = request.get_json()
        old_password = data['old_password']
        new_password = data['new_password']
        if user.password == generate_password_hash(old_password):
            # The user does know the old password
            user.__setattr__('password', new_password)
            user.save()
            logger.info(f'Password changed successfully for user {user.id}')
            return jsonify({}), 200
        else:
            logger.error(f'User {user.id}provided invalid old password')
            return jsonify({'error': 'invalid password'}), 400
    except AttributeError as e:
        logger.exception(e)
        return jsonify({'error': 'not found'}), 404
    except Exception as e:
        logger.exception(e)
        return jsonify({'error': 'not a JSON'}), 400


@api_views.delete('/users/me', strict_slashes=False)
@token_required
def delete_user(email):
    """Delete a user's account"""
    try:
        user = User.get_user_by_email(email)
        user.delete()
        logger.info(f'User {user.id} deleted successfully')
        return jsonify({}), 204
    except AttributeError as e:
        logger.exception(e)
        return jsonify({'error': 'Not Found'}), 404
