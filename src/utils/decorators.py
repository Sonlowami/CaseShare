#!/usr/bin/python3
"""This module contains decorator functions for the views. These includes:
- token_required
"""
import jwt
from functools import wraps
from flask import request, make_response
from os import environ
from flask import jsonify

SECRET_KEY = environ.get('SECRET_KEY')


def token_required(f):
    """Checks if a token is passed by the front-end to the endpoint"""
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        token = token.split(' ')[1].strip() if token else None
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            user_email = data['email']
            return f(user_email, *args, **kwargs)
        except AttributeError:
            response = make_response(jsonify({'error': 'token is missing'}), 403)
            response.headers['location'] = 'http://0.0.0.0:5000/login'
            return response
        except Exception as e:
            print(e)
            response = make_response(jsonify({'error': 'invalid token'}), 403)
            response.headers['location'] = 'http://0.0.0.0:5000/login'
            return response
    return decorator