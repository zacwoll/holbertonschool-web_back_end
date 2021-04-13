#!/usr/bin/env python3
""" Basic Flask App """
from auth import Auth
from flask import abort, Flask, jsonify, redirect, request
from flask.helpers import make_response
from sqlalchemy.orm.exc import NoResultFound
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=["GET"], strict_slashes=False)
def hello():
    """ Returns a greeting """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"], strict_slashes=False)
def users():
    """ Register new users route """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"}), 200


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login():
    """ Login a user to a session """
    email = request.form.get("email")
    password = request.form.get("password")
    valid_user = AUTH.valid_login(email, password)
    if not valid_user:
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout():
    """ Logs a user out a session """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        return abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile')
def profile():
    """ Returns a users profile """
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is NOne:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """ Gets a new reset_token for a user to reset password """
    email = request.form.get('email')

    session = AUTH.create_session(email)
    if session is None:
        abort(403)

    token = AUTH.get_reset_password_token(email)
    return jsonify({"email": email, "reset_token": token}), 200


@app.route('/reset_password', methods=["PUT"])
def update_password():
    """ Updates user password """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_pass = request.form.get('new_password')

    try:
        session = AUTH.create_session(email)
        user = AUTH.get_user_from_session_id(session)
        AUTH.update_password(reset_token, new_pass)
    except Exception:
        abort(403)

    return jsonify({"email": user.email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
