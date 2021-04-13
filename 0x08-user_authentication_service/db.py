#!/usr/bin/env python3
""" This module creates the database ORM """
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """ Database connection to SQLite via SQLAlchemy """

    def __init__(self):
        """ Instantiate DB Engine """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ This method adds a user to the DB """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Returns first User in DB matching kwargs """
        if not kwargs:
            raise InvalidRequestError
        if not all(key in User.__table__.columns for key in kwargs):
            raise InvalidRequestError
        row = self._session.query(User).filter_by(**kwargs).one()
        if not row:
            raise NoResultFound
        return row

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates a user with kwargs in the DB """
        user = self.find_user_by(id=user_id)

        for key in kwargs:
            if key not in user.__dir__():
                raise ValueError
            setattr(user, key, kwargs[key])

        self._session.commit()
        return None
