#!/usr/bin/env python3
""" This module creates the database ORM """
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import TypeVar

from user import Base
from user import User


class DB:

    def __init__(self):
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str):  # -> TypeVar(User):
        """ """
        new_user = User(email, hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> TypeVar(User):
        """ """
        found_user = self._session.query(User).filter_by(**kwargs).one()
