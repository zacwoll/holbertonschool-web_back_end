#!/usr/bin/env python3
""" Authentication Module """
from flask import request
from typing import List, TypeVar


class Auth():
    """ Authentication Object """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require Authentication """
        if not path:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != "/":
            path += "/"
        if path in excluded_paths:
            return False
        else:
            return True


    def authorization_header(self, request=None) -> str:
        """ authorization header """
        if request is None:
            return None
        try:
            auth = request.headers['Authorization']
        except KeyError:
            return None
        return auth


    def current_user(self, request=None) -> TypeVar('User'):
        return None


if __name__ == "__main__":
    a = Auth()
    print(a.require_auth(None, None))
    print(a.require_auth(None, []))
    print(a.require_auth("/api/v1/status/", []))
    print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
    print(a.require_auth("/api/v1/status", ["/api/v1/status/"]))
    print(a.require_auth("/api/v1/users", ["/api/v1/status/"]))
    print(a.require_auth("/api/v1/users", ["/api/v1/status/", "/api/v1/stats"]))
