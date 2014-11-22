# -*- coding: utf-8 -*-
"""
Basic web application to view data collected by the weather station.
"""

import os, time, json
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


def get_peak_wind_speed(time_from, time_to):
    """
    Gets the peak wind speed recorded in a given time.

    @param time_from Start time
    @param time_to End time
    @return Peak wind speed over the time range
    """

    # Get data from database
    db = get_db()
    db.row_factory = list_factory
    cur = db.execute("SELECT peak_wind_speed FROM weather_history WHERE timestamp <= DATETIME(%d, 'unixepoch') AND timestamp > DATETIME(%d, 'unixepoch') ORDER BY timestamp DESC"
            % (time_to, time_from))
    rows = cur.fetchall()

    # Find the max wind speed for this time
    max_wind_speed = 0;
    for point in rows:
        if point[1] > max_wind_speed:
            max_wind_speed = point[1]

    return max_wind_speed


def list_factory(cursor, row):
    """
    Used to format SQLite rows as lists

    @param cursor Current sursor
    @param row Current row
    @return Row as a list
    """

    d = list()
    for idx, col in enumerate(cursor.description):
        d.insert(idx, row[idx])
    return d


@app.route('/history')
def show_history():
    # Get the columns to be retrieved from the database
    requested_columns = request.args.getlist('data_items')
    if len(requested_columns) > 0:
        columns = requested_columns
    else:
        columns = ['temperature', 'pressure']

    # Always need the first column to be timestamp
    columns.insert(0, 'timestamp')

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

    # Get data from database
    db = get_db()
    db.row_factory = list_factory
    cur = db.execute("SELECT %s FROM weather_history WHERE timestamp <= DATETIME(%d, 'unixepoch') AND timestamp > DATETIME(%d, 'unixepoch') ORDER BY timestamp DESC"
            % (','.join(columns), timestamp_to, timestamp_from))
    rows = cur.fetchall()

    column_name_to_label = {
                'timestamp' : 'Timestamp',
                'temperature' : 'Temperature',
                'humidity' : 'Humidity',
                'pressure' : 'Pressure',
                'average_wind_speed' : 'Average Wind Speed',
                'peak_wind_speed' : 'Peak Wind Speed',
                'light_level' : 'Light Level',
                'rain_frequency' : 'Rain'
            }

    # Get friendly column names
    labels = [column_name_to_label[col] for col in columns]

    # Convert the data into a nice format for the template
    data = list()
    for point in rows:
        data.append([point[0], ','.join([str(val) for i, val in enumerate(point) if i > 0])])

    # Get max wind speed over the time range
    max_wind_speed = get_peak_wind_speed(timestamp_to, timestamp_from)

    return render_template('show_history.html', data=data, labels=labels,
                           peak_wind_speed=max_wind_speed,
                           time_to=requested_to, time_from=requested_from,
                           selected_columns=columns)
