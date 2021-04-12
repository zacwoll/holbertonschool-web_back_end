#!/usr/bin/env python3
""" Basic Flask App """
from auth import Auth
from flask import abort, Flask, jsonify, redirect, request
from flask.helpers import make_response
from sqlalchemy.orm.exc import NoResultFound
app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def hello():
    """ Returns a greeting """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"])
def users():
    """ Register new /users route """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        new_user = AUTH.register_user(email, password)
        if new_user is not None:
            return jsonify({"email": email,
                            "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"])
def login():
    """ Login a user to a session """
    email = request.form.get("email")
    password = request.form.get("password")
    valid_user = AUTH.valid_login(email, password)
    if valid_user:
        session_id = AUTH.create_session(email)
        if session_id is not None:
            response = make_response(
                jsonify({"email": email, "message": "logged in"}))
            response.set_cookie("session_id", session_id)
            return response
    else:
        abort(401)


@app.route('/sessions', methods=["DELETE"])
def logout():
    """ Logs a user out a session """
    session_id = request.cookies.get("session_id")
    if session_id is not None:
        user = AUTH.get_user_from_session_id(session_id)
        if user is not None:
            AUTH.destroy_session(user.id)
            return redirect('/')
    return abort(403)


@app.route('/profile')
def profile():
    """ Returns a users profile """
    session_id = request.cookies.get("session_id")
    if session_id is not None:
        user = AUTH.get_user_from_session_id(session_id)
        if user is not None:
            return jsonify({"email": user.email})
    return abort(403)


@app.route('/reset_password', methods=["POST"])
def get_reset_password_token():
    """ Gets a new reset_token for a user to reset password """
    email = request.form.get("email")
    try:
        AUTH._db.find_user_by(email=email)
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except NoResultFound:
        abort(403)


@app.route('/reset_password', methods=["PUT"])
def update_password():
    """ Updates user password """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH._db.find_user_by(email=email)
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
