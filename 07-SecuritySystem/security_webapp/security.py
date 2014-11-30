# -*- coding: utf-8 -*-
"""
Web application to manage several secutriy sensors over MQTT.
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
    PASSWORD='default',
    MQTT_BROKER='localhost'
))
app.config.from_envvar('SECURITY_APP_SETTINGS', silent=True)


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


def dict_factory(cursor, row):
    """
    Used to format SQLite rows as dictionaries

    @param cursor Current sursor
    @param row Current row
    @return Row as a list
    """

    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


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

    try:
        db.commit()
        flash('Deleted sensor %d.' % int(sensor_id))
    except Exception as sql_ex:
        db.rollback()
        flash('Error deleting sensor: %s' % str(sql_ex))

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
            flash('Sensor %d does not exist' % int(sensor_id))
            return redirect(url_for('show_sensors'))

        return render_template('edit_sensor.html', sensor=sensor)

    try:
        cur = db.execute('UPDATE sensors SET name = ?, description = ?, location = ?, mqtt_topic = ?, trigger_text = ? WHERE id = ?',
                         (request.form['sensor_name'], request.form['sensor_description'], request.form['sensor_location'],
                          request.form['sensor_mqtt_topic'], request.form['sensor_trigger_text'], sensor_id))

        db.commit()
        flash('Sensor %d updated.' % int(sensor_id))

    except Exception as sql_ex:
        db.rollback()
        flash('Error updating sensor: %s' % str(sql_ex))

    return redirect(url_for('update_sensor', sensor_id=sensor_id))


@app.route('/sensors/add', methods=['POST', 'GET'])
def add_sensor():
    if not session.get('logged_in'):
        abort(401)

    if request.method == 'GET':
        return render_template('edit_sensor.html', sensor=None)

    db = get_db()

    try:
        cur = db.execute('INSERT INTO sensors (name, description, location, mqtt_topic, trigger_text) VALUES (?, ?, ?, ?, ?)',
                         (request.form['sensor_name'], request.form['sensor_description'], request.form['sensor_location'],
                          request.form['sensor_mqtt_topic'], request.form['sensor_trigger_text']))
        sensor_id = cur.lastrowid

        db.commit()
        flash('Added sensor %d.' % int(sensor_id))
        return redirect(url_for('update_sensor', sensor_id=sensor_id))

    except Exception as sql_ex:
        db.rollback()
        flash('Error adding sensor: %s' % str(sql_ex))
        return redirect(url_for('add_sensor'))


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

    try:
        db.commit()
        flash('Deleted event %d.' % int(event_id))
    except Exception as sql_ex:
        db.rollback()
        flash('Error deleting event: %s' % str(sql_ex))

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

    try:
        db.commit()
        flash('Deleted alarm %d.' % int(alarm_id))
    except Exception as sql_ex:
        db.rollback()
        flash('Error deleting alarm: %s' % str(sql_ex))

    return redirect(url_for('show_alarms'))


@app.route('/alarms/<alarm_id>', methods=['POST', 'GET'])
def update_alarm(alarm_id):
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    # If we just want to look at the alarm
    if request.method == 'GET':
        cur = db.execute('SELECT * FROM alarms WHERE id = ?', (alarm_id,))
        alarm = cur.fetchone()

        # Give an error if the alarm does not exist
        if alarm is None:
            flash('Alarm with ID %d does not exist' % int(alarm_id))
            return redirect(url_for('show_sensors'))

        # Get all of the sensors for this alarm
        sensors = get_sensors_input(alarm_id)

        return render_template('edit_alarm.html', alarm=alarm, sensors=sensors)

    # Here we are updating the alarm
    try:
        # Update the alarm entry
        cur = db.execute('UPDATE alarms SET name = ?, description = ?, alert_when = ? WHERE id = ?',
                         (request.form['alarm_name'], request.form['alarm_description'], request.form['alarm_alert_when'], alarm_id))

        # Remove all existing mapping between the alarm and sensors
        db.execute('DELETE FROM alarm_has_sensor WHERE alarm_id = ?', (alarm_id,))

        # For each of the currently enabled sensors add a mapping in the database
        enabled_sensor_ids = request.values.getlist('enabled_sensors')
        for sensor_id in enabled_sensor_ids:
            db.execute('INSERT INTO alarm_has_sensor (alarm_id, sensor_id) VALUES (?, ?)', (alarm_id, sensor_id))

        db.commit()
        flash('Alarm %d updated.' % int(alarm_id))

    except Exception as sql_ex:
        db.rollback()
        flash('Error updating alarm: %s' % str(sql_ex))

    return redirect(url_for('update_alarm', alarm_id=alarm_id))


@app.route('/alarms/add', methods=['POST', 'GET'])
def add_alarm():
    if not session.get('logged_in'):
        abort(401)

    # If just showing the add page
    if request.method == 'GET':
        sensors = get_sensors_input()
        return render_template('edit_alarm.html', alarm=None, sensors=sensors)

    db = get_db()

    # Add the alarm here
    try:
        cur = db.execute('INSERT INTO alarms (name, description, alert_when) VALUES (?, ?, ?)',
                         (request.form['alarm_name'], request.form['alarm_description'], request.form['alarm_alert_when']))
        alarm_id = cur.lastrowid

        # For each of the currently enabled sensors add a mapping in the database
        enabled_sensor_ids = request.values.getlist('enabled_sensors')
        for sensor_id in enabled_sensor_ids:
            db.execute('INSERT INTO alarm_has_sensor (alarm_id, sensor_id) VALUES (?, ?)', (alarm_id, sensor_id))

        db.commit()
        flash('Added alarm %d.' % int(alarm_id))
        return redirect(url_for('update_alarm', alarm_id=alarm_id))

    except Exception as sql_ex:
        db.rollback()
        flash('Error adding alarm: %s' % str(sql_ex))
        return redirect(url_for('add_alarm'))


def get_sensors_input(alarm_id=None):
    """
    Gets information about sensors associated with an alarm.

    @param alarm_id ID of alarm to get sensors for
    """

    db = get_db()
    db.row_factory = dict_factory
    cur = db.execute('SELECT id, name FROM sensors')
    sensors = cur.fetchall()

    enabled_sensor_ids = list()
    if alarm_id is not None:
        cur = db.execute('SELECT sensor_id FROM alarm_has_sensor WHERE alarm_id = ?', (alarm_id,))
        enabled_sensor_ids = [ s['sensor_id'] for s in cur.fetchall() ]

    for s in sensors:
        s['enabled'] = s['id'] in enabled_sensor_ids

    return sensors


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
