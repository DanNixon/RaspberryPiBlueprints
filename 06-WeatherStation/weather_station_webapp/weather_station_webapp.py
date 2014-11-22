# -*- coding: utf-8 -*-
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
                  render_template, flash

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'weather.db'),
    DEBUG=True,
    SECRET_KEY='development key'
))
app.config.from_envvar('WEATHER_SETTINGS', silent=True)


def connect_db():
    """
    Connects to the specific database.
    """
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """
    Initializes the database.
    """
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """
    Creates the database tables.
    """
    init_db()
    print('Initialized the database.')


def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """
    Closes the database again at the end of the request.
    """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_current():
    db = get_db()
    cur = db.execute('SELECT * FROM weather_history ORDER BY timestamp DESC LIMIT 1')
    data = cur.fetchone()
    return render_template('show_current.html', data=data)


@app.route('/history')
def show_history():
    db = get_db()
    cur = db.execute('SELECT wind_direction, wind_speed FROM weather_history ORDER BY timestamp DESC')
    data = cur.fetchall()
    return render_template('show_history.html', data=data)
