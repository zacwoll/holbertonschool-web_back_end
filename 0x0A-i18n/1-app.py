#!/usr/bin/env python3
""" Basic Flask App """
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """ Config class """
    LANGUAGES = ['en', 'fr']


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)
babel = Babel(app)
Babel.default_locale = 'en'
Babel.default_timezone = 'UTC'


@app.route('/', methods=["GET"])
def default_route():
    """ Returns a greeting """
    return render_template('1-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
