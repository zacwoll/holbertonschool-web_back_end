#!/usr/bin/env python3
""" Authentication Module """
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """ bcrypt hash method """
    import bcrypt
    return bcrypt.hashpw(password.encode(),
                         bcrypt.gensalt()).decode('utf-8')


def _generate_uuid() -> str:
    """ uuid generation method """
    from uuid import uuid4
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a user in the DB """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None

        if user:
            raise ValueError(f"User {user.email} already exists")

        hashed_password = _hash_password(password)

        return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """ Validate Login """
        import bcrypt
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode(),
                              user.hashed_password.encode())

    def create_session(self, email: str) -> str:
        """ Creates a session for the user, returns session_id """
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
        except NoResultFound:
            return None
        return session_id

    def get_user_from_session_id(self, session_id: str) -> str:
        """ Finds a user with a session_id """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """ Removes a session_id, ending the session """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ generates a reset password token """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates a user password to a provided password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=hash_pass,
            reset_token=None
        )
        return None
