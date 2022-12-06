#!/usr/bin/python3
"""
Database Storage System
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """
        create the engine (self.__engine)
        """
        username = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV")
        url = f"mysql+mysqldb://{username}:{password}@{host}:3306/{db}"
        self.__engine = create_engine(url, pool_pre_ping=True)
        if env == "test":
            conn = self.__engine.connect()
            tables = conn.execute("SHOW TABLES")
            for table in tables.fetchall():
                conn.execute(f"DROP TABLE IF EXISTS {table[0]}")

    def all(self, cls=None):
        """
        query on the current database session (self.__session) all objects
        depending of the class name (argument cls)
        if cls=None, query all types of objects (User, State, City,
        Amenity, Place and Review)
        this method must return a dictionary: (like FileStorage)
        key = <class-name>.<object-id>
        value = object
        """
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        obj = {}
        map_classes = {
                    'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                }
        if cls:
            for data in self.__session.query(map_classes[cls.__name__]).all():
                key = f"{cls.__name__}.{data.id}"
                obj[key] = data
        else:
            """
            cls = ("User", "State", "City",
                    "Amenity", "Place", "Review")
            """
            cls = ("State", "City", "User", "Place")
            for c in cls:
                for data in self.__session.query(map_classes[c]).all():
                    key = f"{c}.{data.id}"
                    obj[key] = data
        return obj

    def new(self, obj):
        """
         add the object to the current database session (self.__session)
        """
        self.__session.add(obj)

    def save(self):
        """
        commit all changes of the current database session (self.__session)
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete from the current database session obj if not None
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        from models.base_model import Base
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
