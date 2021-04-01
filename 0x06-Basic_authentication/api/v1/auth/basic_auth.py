#!/usr/bin/env python3
""" Basic Authentication Module """
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ Basic Authentication Object """

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """ Accept authorization and validate """
        if authorization_header is None:
            return None

        if isinstance(authorization_header, str) is False:
            return None

        try:
            auth_type, auth_str = authorization_header.split(' ')
            if auth_type != 'Basic':
                return None
        except ValueError:
            return None

        return auth_str

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """ decode valid auth payload """
        from base64 import b64decode

        if base64_authorization_header is None:
            return None

        value = base64_authorization_header

        if isinstance(value, str) is False:
            return None

        try:
            return b64decode(value).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """ Extract user credentials from encoded auth payload """

        if decoded_base64_authorization_header is None:
            return None, None

        if isinstance(decoded_base64_authorization_header, str) is False:
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, pwd = decoded_base64_authorization_header.split(':')
        return email, pwd

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """ Create User from credentials """

        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        user = User(email=user_email, _password=user_pwd)

        result = user.search({"email": user_email})
        if result == []:
            user = None
        else:
            user = result[0]

        if user is None:
            return None

        if user.is_valid_password(user_pwd):
            return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Determine if Authorization is successful
        if yes, Create User and send to API """
        header = self.authorization_header(request)
        b64pwd = self.extract_base64_authorization_header(header)
        user_cred = self.decode_base64_authorization_header(b64pwd)
        email, pwd = self.extract_user_credentials(user_cred)
        user = self.user_object_from_credentials(email, pwd)
        return user
