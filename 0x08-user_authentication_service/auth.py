#!/usr/bin/env python3
""" Authentication Module """
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar, Union
from user import User
from uuid import uuid4


def _hash_password(password: str) -> str:
    """ bcrypt hash method """
    return bcrypt.hashpw(password.encode(),
                         bcrypt.gensalt()).decode('utf-8')


def _generate_uuid() -> str:
    """ uuid generation method """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar(User):
        """ Registers a user in the DB """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """ Validate Login """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(password.encode(),
                                      user.hashed_password.encode())
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Creates a session for the user, returns session_id """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                session_id = _generate_uuid()
                user_data = {"session_id": session_id}
                self._db.update_user(user.id, **user_data)
                return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """ Finds a user based on a session_id """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Removes a session_id, ending the session """
        try:
            user = self._db.find_user_by(id=user_id)
            user_data = {"session_id": None}
            self._db.update_user(user.id, **user_data)
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ generates a reset password token """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates a user password to a provided password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            user_data = {"hashed_password": hashed_password,
                         "reset_token": None}
            self._db.update_user(user.id, **user_data)
            return None
        except NoResultFound:
            raise ValueError
