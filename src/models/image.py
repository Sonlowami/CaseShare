#!/usr/bin/python
""" holds class image"""
from .base_model import BaseModel
from utils.database import db


class Image(BaseModel, db.Model):
    """Representation of image"""
    __tablename__ = "images"
    filename = db.Column(db.String(100), nullable=False)
    post_id = db.Column(db.String(60), db.ForeignKey("posts.id"), nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    
