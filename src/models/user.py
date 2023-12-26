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
    sex = db.Column(db.String(10))
    age = db.Column(db.Integer, default=0)
    reset_token = db.Column(db.String(256))
    otp = db.Column(db.Integer, default=0)
    otp_expiry = db.Column(db.DateTime)
    images = db.relationship("Image", backref="user", cascade="all, delete, delete-orphan")
    videos = db.relationship("Video", backref="user", cascade="all, delete, delete-orphan")
    posts = db.relationship("Post", backref="user", cascade="all, delete, delete-orphan")
    likes = db.relationship("Like", backref="user", cascade="all, delete, delete-orphan")
    comments = db.relationship("Comment", backref="user", cascade="all, delete, delete-orphan")
    documents = db.relationship("Document", backref="user", cascade="all, delete, delete-orphan")

    def __setattr__(self, __name: str, __value: Any):
        """Set attributes of the user"""
        if __name == 'password':
            super.__setattr__(self, __name, generate_password_hash(__value))
        else:
            super.__setattr__(self, __name, __value)

    def to_dict(self):
        """Return a dictionary representation of the user"""
        user_dict = super().to_dict()
        user_dict.pop('password', None)
        user_dict.pop('reset_token', None)
        user_dict.pop('otp', None)
        user_dict.pop('otp_expiry', None)
        return user_dict

    @staticmethod
    def get_user_by_email(email: str) -> 'User':
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_all_users() -> list:
        return User.query.all()
