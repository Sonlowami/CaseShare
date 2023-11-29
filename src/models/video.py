#!/usr/bin/python
""" holds class video"""
from .base_model import BaseModel
from  utils.database import db

class Video(BaseModel, db.Model):
    """Representation of videos"""

    __tablename__ = "videos"
    filename = db.Column(db.String(100), nullable=False)
    post_id = db.Column(db.String(60), db.ForeignKey("posts.id"), nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
