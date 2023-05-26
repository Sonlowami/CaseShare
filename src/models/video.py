#!/usr/bin/python
""" holds class video"""
from .base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey

class Video(BaseModel, Base):
    """Representation of videos"""

    __tablename__ = "videos"
    filename = Column(String(100), nullable=False)
    post_id = Column(String(60), ForeignKey("posts.id"), nullable=False)