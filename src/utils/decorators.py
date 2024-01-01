#!/usr/bin/python3
"""This module contains decorator functions for the views. These includes:
- token_required
"""
import jwt
from functools import wraps
from flask import request, make_response
from os import environ
from flask import jsonify
from utils.logger import logger

SECRET_KEY = environ.get('SECRET_KEY')


def token_required(f):
    """Checks if a token is passed by the front-end to the endpoint"""
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            token = token.split(' ')[1].strip() if token else None
            data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            user_email = data['email']
            logger.info('Token validated successfully')
            return f(user_email, *args, **kwargs)
        except Exception as e:
            logger.exception(e)
            response = make_response(jsonify({'error': 'invalid or missing token'}), 403)
            return response
    return decorator