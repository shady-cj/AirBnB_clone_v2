#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table

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

    @property
    def reviews(self):
        """ getter for reviews"""
        return self.reviews

    @property
    def amenities(self):
        """ Getter for filestorage """
        self.amenities

    @amenities.setter
    def amenities(self, a):
        """ Setter for filestorage """
        if type(a).__name__ == "Amenity":
            self.amenities.append(a.id)
