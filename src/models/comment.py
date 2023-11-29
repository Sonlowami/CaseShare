#!/usr/bin/python
"""holds calss comment"""
from .base_model import BaseModel
from utils.database import db

class Comment(BaseModel, db.Model):
    """Representation of comment"""
    __tablename__ = "comments"
    content = db.Column(db.String(512), nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.String(60), db.ForeignKey("posts.id"), nullable=False)