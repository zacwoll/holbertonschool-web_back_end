#!/usr/bin/env python3
""" Basic Flask App """
from babel.dates import format_datetime
from datetime import datetime
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz


class Config:
    """ Config class """
    LANGUAGES = ['en', 'fr']


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)

babel = Babel(app)
Babel.default_locale = 'en'
Babel.default_timezone = 'UTC'


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@app.route('/', methods=["GET"])
def default_route():
    """ Returns a greeting """
    time = format_datetime(datetime.now(get_timezone()), locale=get_locale())
    return render_template('index.html', user=g.user, current_time=time)


@babel.localeselector
def get_locale():
    """ Get local from request """
    locale = request.args.get('locale')
    if locale in Config.LANGUAGES:
        return locale
    user = request.args.get('login_as')
    if user:
        locale = get_user(user).get('locale')
        if locale in Config.LANGUAGES:
            return locale
    header = request.headers.get('locale')
    if header:
        return header
    return request.accept_languages.best_match(Config.LANGUAGES)


@babel.timezoneselector
def get_timezone():
    """ Get timezone from request """
    tz = request.args.get('timezone')
    if tz:
        try:
            return pytz.timezone(tz)
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    if g.user:
        tz = g.user.get('timezone')
        if tz:
            try:
                return pytz.timezone(tz)
            except pytz.exceptions.UnknownTimeZoneError:
                pass
    return pytz.timezone('utc')


def get_user(user):
    """ Login user or None if cannot be found """
    if user and int(user) in users:
        return users.get(int(user))


@app.before_request
def before_request():
    """ Allow login """
    g.user = get_user(request.args.get('login_as'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
