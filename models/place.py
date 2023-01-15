#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table
import os

place_amenity = Table("place_amenity", Base.metadata,
                Column("place_id", String(60), ForeignKey("places.id"), primary_key=True),
                Column("amenity_id", String(60), ForeignKey("amenities.id"), primary_key=True)
                )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", cascade="all, delete, delete-orphan",
                           backref="place")
    amenities = relationship("Amenity", secondary=place_amenity, viewonly=False,
                             backref="place_amenities")
    amenity_ids = []

    if os.getenv("HBNB_TYPE_STORAGE") != "db": 
        @property
        def reviews(self):
            """ getter for reviews"""
            from models import storage
            from models.review import Review
            r = []
            for v in storage.all(Review).values():
                if v.place_id == self.id:
                    r.append(v)
            return r

        @property
        def amenities(self):
            """ Getter for filestorage """
            from models import storage
            from models.amenity import Amenity
            am = []
            for v in storage.all(Amenity).values():
                if v.id in self.amenity_ids:
                    am.append(v)
            return am

        @amenities.setter
        def amenities(self, a):
            """ Setter for filestorage """
            if type(a).__name__ == "Amenity":
                if "amenity_ids" in self.__dict__:
                    self.amenity_ids.append(a.id)
                else:
                    self.amenity_ids = [a.id]
