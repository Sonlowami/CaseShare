#!/usr/bin/python
""" holds class direct_message"""
from .base_model import BaseModel
from utils.database import db

class Message(BaseModel, db.Model):
     """Representation of direct message"""
     __tablename__ = "messages"
     content = db.Column(db.String(512), nullable=False)
     sender_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
     receiver_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)

     sender = db.relationship("User", foreign_keys=[sender_id])
     receiver = db.relationship("User", foreign_keys=[receiver_id])
