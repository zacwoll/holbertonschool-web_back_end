#!/usr/bin/env python3
""" All routes for session authentication """
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ Login route """
    from models.user import User
    from api.v1.app import auth
    from os import getenv

    email = request.form.get('email')
    pwd = request.form.get('password')

    if email is None:
        return jsonify({"error": "email missing"}), 400

    if pwd is None:
        return jsonify({'error': 'password missing'}), 400

    search_results = User().search({'email': email})
    if search_results == []:
        return jsonify({'error': 'no user found for this email'}), 404
    user = next((account for account in search_results
                if account.is_valid_password(pwd)), None)
    if user is None:
        return jsonify({'error': 'wrong password'}), 401

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(getenv('SESSION_NAME'), session_id)

    return response


@app_views.route(
    '/auth_session/logout',
    methods=['DELETE'],
    strict_slashes=False
)
def logout() -> str:
    """ logout route """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
