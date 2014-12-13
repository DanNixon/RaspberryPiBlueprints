# -*- coding: utf-8 -*-
"""
Web application to control servos for a robot arm via RPi GPIO.
"""

import os, logging
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template
from RPIO import PWM


app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,

    LOG_FILE='robot_arm.log',
    LOG_LEVEL='DEBUG',

    LEFT_C_SERVO_GPIO=None,
    RIGHT_C_SERVO_GPIO=None,
    ARM_1_SERVO_GPIO=None,
    ARM_2_SERVO_GPIO=None,
    GRIP_SERVO_GPIO=None,

    LEFT_C_SERVO_MIN=600,
    RIGHT_C_SERVO_MIN=600,
    ARM_1_SERVO_MIN=600,
    ARM_2_SERVO_MIN=600,
    GRIP_SERVO_MIN=600,

    LEFT_C_SERVO_MAX=2500,
    RIGHT_C_SERVO_MAX=2500,
    ARM_1_SERVO_MAX=2500,
    ARM_2_SERVO_MAX=2500,
    GRIP_SERVO_MAX=2500
))
app.config.from_envvar('ROBOT_ARM_SETTINGS', silent=True)


log_level = getattr(logging, app.config['LOG_LEVEL'].upper(), None)
logging.basicConfig(level=log_level, filename=app.config['LOG_FILE'])

SERVO_POSITIONS = dict()
SERVOS = dict()


def set_servo(servo_id, position):
    """
    Sets a given GPIO.

    @param servo_id ID of servo to set
    @param position Timing value for servo position, will be rounded to nearest 10us
    """

    time_val = int(round(position, -1))
    gpio = app.config[servo_id + '_GPIO']

    # Create a new servo object if it does not exist
    if servo_id not in SERVOS:
        SERVOS[servo_id] = PWM.Servo()

    servo = SERVOS[servo_id]

    logging.getLogger(__name__).debug('Setting servo %s on GPIO %d: value %d' % (servo_id, gpio, time_val))
    servo.set_servo(gpio, time_val)

    # Record the position of the sensor
    SERVO_POSITIONS[servo_id] = time_val


def set_servos_default():
    """
    Sets all servos to their default position.
    """
    logging.getLogger(__name__).info('Resetting servos to default position')

    set_servo('LEFT_C_SERVO', 600)
    set_servo('RIGHT_C_SERVO', 600)
    set_servo('ARM_1_SERVO', 600)
    set_servo('ARM_2_SERVO', 600)
    set_servo('GRIP_SERVO', 600)


@app.route('/')
def show_control():
    return render_template('control.html')


@app.route('/control_w_video')
def show_control_with_video():
    return render_template('control_w_video.html')


@app.route('/video')
def show_video():
    return render_template('video.html')


@app.route('/command/<command>')
def handle_command(command):
    logging.getLogger(__name__).debug('Got command: %s' % command)

    # TODO

    return redirect(url_for('show_control'))


# Set servos to default position when app starts
set_servos_default()
