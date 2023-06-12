#!/usr/bin/python3
"""This module contains decorator functions for the views. These includes:
- token_required
"""
import jwt
from functools import wraps
from flask import request
from os import environ
from flask import jsonify

SECRET_KEY = environ.get('SECRET_KEY')


def token_required(f):
    """Checks if a token is passed by the front-end to the endpoint"""
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('x-token')
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            user_email = data['email']
            return f(user_email, *args, **kwargs)
        except AttributeError:
            return jsonify({'error': 'token is missing'}), 403
        except Exception:
            return jsonify({'error': 'invalid token'}), 403
    return decorator
                