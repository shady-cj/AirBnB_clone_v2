#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import String, Column, DateTime


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {
            'mysql_default_charset': 'latin1',
            }

Base = declarative_base(cls=Base)


class BaseModel:
    id = Column(String(60), primary_key=True, default=uuid.uuid4, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    """A base class for all hbnb models"""
    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at= datetime.utcnow()
        if kwargs:
            for att in kwargs.keys():
                if att != "__class__":
                    if att in ("created_at", "updated_at"):
                        dateobj = datetime.fromisoformat(kwargs[att])
                        setattr(self, att, dateobj)
                    else:
                        setattr(self, att, kwargs[att])

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        cls_dict = dict(self.__dict__)
        if cls_dict.get("_sa_instance_state"):
            cls_dict.pop("_sa_instance_state")

        return '[{}] ({}) {}'.format(cls, self.id, cls_dict)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if dictionary.get("_sa_instance_state"):
            dictionary.pop("_sa_instance_state")
        return dictionary

    def delete(self):
        from models import storage
        storage.delete()
