#!/usr/bin/python
""" holds class document"""
from .base_model import BaseModel
from utils.database import db

class Document(BaseModel, db.Model):
    """Representation of document"""
    __tablename__ = "documents"
    filename = db.Column(db.String(100), nullable=False)
    post_id = db.Column(db.String(60), db.ForeignKey("posts.id"), nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
