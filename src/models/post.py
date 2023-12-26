#!/usr/bin/python
"""hold class post """
from .base_model import BaseModel
from utils.database import db


class Post(BaseModel, db.Model):
    """Reperesentation of post"""
    __tablename__ = "posts"
    user_id = db.Column(db.String(60), db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(2048), nullable=False)
    comments = db.relationship("Comment", backref="post", cascade="all, delete, delete-orphan")
    likes = db.relationship("Like", backref="like", cascade="all, delete, delete, delete-orphan")