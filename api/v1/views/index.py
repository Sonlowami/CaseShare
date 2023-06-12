#!/usr/bin/python3
"""This module contain some view functions for our APIs.
Particularly, the one for status, and all the views needed to manage user sessions"""
from flask import jsonify
from os import environ
from api.v1.views import api_views

secret_key=environ.get('SECRET_KEY')

@api_views.get('/status', strict_slashes=False)
def status():
    """Return the status of the API"""
    return jsonify({'status': 'OK'}), 200