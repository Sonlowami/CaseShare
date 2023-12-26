#!/usr/bin/python
from .base_model import BaseModel
from utils.database import db

class Like(BaseModel, db.Model):
    """Representation of likes"""

    __tablename__ = "likes"
    user_id = db.Column(db.String(60), db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.String(60), db.ForeignKey("posts.id"), nullable=False)
