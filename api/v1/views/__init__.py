#!/usr/bin/python3
"""This module defines a blueprint on which we will map our view functions"""
from flask import Blueprint

api_views = Blueprint('api_views', __name__, url_prefix='/our-apis/v1/')

from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.posts import *
from api.v1.views.comment import *
