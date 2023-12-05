#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
from utils.database import db
import uuid

time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """The BaseModel class from which future classes will be derived"""

    id = db.Column(db.String(60), primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        setattr(self, 'id', str(uuid.uuid4()))
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        """Define a base way to print models"""
        return f"{self.__class__.__name__} <{self.id}>"

    def to_dict(self):
        """Define a base way to jsonify models, dealing with datetime objects"""
        dict = {}
        for column in self.__table__.columns:
            if isinstance(getattr(self, column.name), datetime):
                dict[column.name] = getattr(self, column.name).strftime(time)
            else:
                dict[column.name] = getattr(self, column.name)
        try:
            del dict['filepath']
        except KeyError:
            pass
        return dict

    def save(self):
        """Save an object to the database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delete(self):
        """Delete an object from the database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
                          