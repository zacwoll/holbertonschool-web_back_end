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
        for excluded_path in excluded_paths:
            if path in excluded_paths:
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
