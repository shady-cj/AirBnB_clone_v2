#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey

class City(BaseModel, Base):
    __tablename__ = "cities"
    """ The city class, contains state ID and name """
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    name = Column(String(128), nullable=False)

