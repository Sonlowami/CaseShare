#!/usr/bin/python3
"""This file contain views that define endpoints used to interact with user
authentication."""
from flask import jsonify, request, redirect, make_response
import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from os import environ
from api.v1.views import api_views
from datetime import timedelta, datetime
from models.user import User
from flasgger.utils import swag_from
from utils.decorators import token_required

SECRET_KEY = environ.get("SECRET_KEY")

@api_views.post('/users/auth/login', strict_slashes=False)
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
    except Exception as e:
        print(e)
        return jsonify({'error': 'Not a JSON'}), 400

@api_views.post('/users/auth/register', strict_slashes=False)
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
        gender = user_data.get('sex')
        age = user_data.get('age')
        title = user_data.get('title')
        phone = user_data.get('phone')
        new_user = User(email=email, password=password, first_name=first_name,
                        last_name=last_name, sex=gender, country=country, age=age, title=title, phone=phone)
        new_user.save()
        return jsonify({'email': new_user.email}), 201
    except KeyError:
        return jsonify({'error': 'Missing some data'}), 400
    except TypeError as err:
        print(err)
        return jsonify({'error': 'Not a JSON'}), 400

    
@api_views.post('/users/auth/forgot_password')
def forgot_password():
    """Send a password reset link to the user's email"""
    try:
        data = request.get_json()
        email = data.get('email')
        user = User.get_user_by_email(email)
        if user:
            # The user exists
            token = jwt.encode({'email': email, 'exp': datetime.utcnow() + timedelta(minutes=15)}, SECRET_KEY)
            user.__setattr__('reset_token', token)
            user.save()
            return jsonify({
                "message": "Password reset link sent to your email",
                "token": f'{request.host_url}api/v1/users/auth/reset_password/{token}'
            }), 200
        else:
            return jsonify({'error': 'Not Found'}), 404
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

@api_views.post('/users/auth/reset_password/<string:token>')
@swag_from('documentation/users/reset_password.yml', methods=['POST'])
def reset_password(token):
    """Reset password"""
    try:
        email = jwt.decode(token, SECRET_KEY, algorithms='HS256')['email']
        user = User.get_user_by_email(email)
        new_password = request.get_json().get('new_password')
        user.__setattr__('password', new_password)
        user.save()
        return jsonify({
            "message": "Password reset successful"
        }), 200
    except AttributeError:
        return jsonify({'error': 'Not Found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'error': 'Not a JSON'}), 400

@api_views.delete('/users/me', strict_slashes=False)
@token_required
def delete_user(email):
    """Delete a user's account"""
    user = User.get_user_by_email(email)
    try:
        user.delete()
        return jsonify({}), 204
    except AttributeError:
        return jsonify({'error': 'Not Found'}), 404    
