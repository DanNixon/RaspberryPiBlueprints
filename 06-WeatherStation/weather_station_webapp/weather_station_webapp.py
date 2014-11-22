# -*- coding: utf-8 -*-
"""
Basic web application to view data collected by the weather station.
"""

import os, time
from datetime import timedelta
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
                  render_template, flash

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'weather.db'),
    DEBUG=True
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
    # Get the requested time range
    requested_from = request.args.get('from_time')
    requested_to = request.args.get('to_time')

    # The format requests from the timestamp window form come in
    request_format = '%Y-%m-%dT%H:%M'

    # Get the end of the time range (defaults to now)
    timestamp_to = int(time.time())
    if requested_to is not None and not requested_to == '':
        timestamp_to = time.mktime(time.strptime(requested_to, request_format))
    else:
        requested_to = time.strftime(request_format, time.gmtime(timestamp_to))

    # Get the start of the time range (defaults to a week before end)
    timestamp_from = timestamp_to - int(timedelta(days=7).total_seconds())
    if requested_from is not None and not requested_from == '':
        timestamp_from = time.mktime(time.strptime(requested_from, request_format))
    else:
        requested_from = time.strftime(request_format, time.gmtime(timestamp_from))

    db = get_db()
    cur = db.execute("SELECT * FROM weather_history WHERE timestamp <= DATETIME(%d, 'unixepoch') AND timestamp > DATETIME(%d, 'unixepoch') ORDER BY timestamp DESC"
            % (timestamp_to, timestamp_from))

    data = cur.fetchall()

    return render_template('show_history.html', data=data, time_to=requested_to, time_from=requested_from)
