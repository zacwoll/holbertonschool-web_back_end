#!/usr/bin/env python3
""" Authentication Module """
from flask import request
from typing import List, TypeVar


class Auth():
    """ Authentication Object """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require Authentication """

        if path is None or excluded_paths is None:
            return True

        if path[-1] != "/":
            path += "/"

        if path in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            if excluded_path[-1] == "*":
                # Matches patterns up to asterisk (*)
                base_pattern = excluded_path[0:-1]
                if base_pattern in path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ authorization header """
        if request is None:
            return None

        for header in request.headers:
            key, value = header
            if key == 'Authorization':
                return value

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Default Overload """
        return None

    def session_cookie(self, request=None):
        """ returns a cookie from a request """
        if request is None:
            return None
        from os import getenv
        session_name = getenv('SESSION_NAME')
        cookie = request.cookies.get(session_name)
        return cookie


if __name__ == "__main__":
    a = Auth()
    print(a.require_auth(None, None))
    print(a.require_auth(None, []))
    print(a.require_auth("/api/v1/status/", []))
    print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
    print(a.require_auth("/api/v1/status", ["/api/v1/status/"]))
    print(a.require_auth("/api/v1/users", ["/api/v1/status/"]))
    print(a.require_auth("/api/v1/users", ["/api/v1/status/",
                                           "/api/v1/stats"]))
