#!/usr/bin/python3
"""holds class User"""

from typing import Any
from .base_model import BaseModel
from utils.database import db
from werkzeug.security import generate_password_hash

class User(BaseModel, db.Model):
    """Representation of a user"""
    __tablename__ = 'users'
    email = db.Column(db.String(128), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    country = db.Column(db.String(128))
    title = db.Column(db.String(256))
    phone = db.Column(db.String(26))
    age = db.Column(db.Integer, default=0)
    images = db.relationship("Image", backref="user", cascade="all, delete, delete-orphan")
    videos = db.relationship("Video", backref="user", cascade="all, delete, delete-orphan")
    posts = db.relationship("Post", backref="user", cascade="all, delete, delete-orphan")
    likes = db.relationship("Like", backref="user", cascade="all, delete, delete-orphan")
    comments = db.relationship("Comment", backref="user", cascade="all, delete, delete-orphan")
    documents = db.relationship("Document", backref="user", cascade="all, delete, delete-orphan")

    def __setattr__(self, __name: str, __value: Any):
        if __name == 'password':
            self.__dict__[__name] = generate_password_hash(__value)
        else:
            super.__setattr__(self, __name, __value)

    @staticmethod
    def get_user_by_email(email: str) -> 'User':
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_all_users() -> list:
        return User.query.all()
