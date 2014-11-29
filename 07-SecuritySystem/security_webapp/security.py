# -*- coding: utf-8 -*-
"""
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'security.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


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
def show_home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    return redirect(url_for('show_sensors'))


@app.route('/sensors')
def show_sensors():
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    cur = db.execute('SELECT * FROM sensors ORDER BY id ASC')
    sensors = cur.fetchall()
    return render_template('show_sensors.html', sensors=sensors)


@app.route('/sensors/<sensor_id>/delete')
def delete_sensor(sensor_id):
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    cur = db.execute('DELETE FROM sensors WHERE id = ?', (sensor_id,))
    db.commit()

    flash('Deleted sensor with ID %d' % int(sensor_id))
    return redirect(url_for('show_sensors'))


@app.route('/sensors/<sensor_id>', methods=['POST', 'GET'])
def update_sensor(sensor_id):
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    if request.method == 'GET':
        cur = db.execute('SELECT * FROM sensors WHERE id = ?', (sensor_id,))
        sensor = cur.fetchone()

        if sensor is None:
            flash('Sensor with ID %d does not exist' % int(sensor_id))
            return redirect(url_for('show_sensors'))

        return render_template('edit_sensor.html', sensor=sensor)

    # TODO

    return redirect(url_for('update_sensor', sensor_id=sensor_id))


@app.route('/sensors/add', methods=['POST', 'GET'])
def add_sensor():
    if not session.get('logged_in'):
        abort(401)

    if request.method == 'GET':
        return render_template('edit_sensor.html', sensor=None)

    # TODO

    return redirect(url_for('update_sensor', sensor_id=0))


@app.route('/events')
def show_events():
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    cur = db.execute('SELECT * FROM events ORDER BY timestamp DESC')
    events = cur.fetchall()
    return render_template('show_events.html', events=events)


@app.route('/events/<event_id>/delete')
def delete_event(event_id):
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    cur = db.execute('DELETE FROM events WHERE id = ?', (event_id))
    db.commit()

    flash('Deleted event with ID %d' % int(event_id))
    return redirect(url_for('show_events'))


@app.route('/alarms')
def show_alarms():
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    cur = db.execute('SELECT * FROM alarms ORDER BY id ASC')
    alarms = cur.fetchall()
    return render_template('show_alarms.html', alarms=alarms)


@app.route('/alarms/<alarm_id>/delete')
def delete_alarm(alarm_id):
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    cur = db.execute('DELETE FROM alarms WHERE id = ?', (alarm_id))
    db.commit()

    flash('Deleted alarm with ID %d' % int(alarm_id))
    return redirect(url_for('show_alarms'))


@app.route('/alarms/<alarm_id>', methods=['POST', 'GET'])
def update_alarm(alarm_id):
    if not session.get('logged_in'):
        abort(401)

    # TODO

    return redirect(url_for('update_alarm', alarm_id))


@app.route('/alarms/add', methods=['POST', 'GET'])
def add_alarm():
    if not session.get('logged_in'):
        abort(401)

    # TODO

    return redirect(url_for('show_alarms'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_home'))
