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

    SERVO_DELTA=50,

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

    # Ignore positions out of the valid range
    if position > app.config[servo_id + '_MAX']:
        return
    if position < app.config[servo_id + '_MIN']:
        return

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

    all_servo_ids = ['LEFT_C_SERVO', 'RIGHT_C_SERVO', 'ARM_1_SERVO', 'ARM_2_SERVO', 'GRIP_SERVO']
    for servo_id in all_servo_ids:
        set_servo(servo_id, app.config[servo_id + '_MIN'])


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

    if command == 'mov_fwd':
        pass
    elif command == 'mov_rev':
        pass
    elif command == 'rot_cw':
        pass
    elif command == 'rot_ccw':
        pass
    elif command == 'stop':
        pass
    elif command == 'arm1_raise':
        set_servo('ARM_1_SERVO', SERVO_POSITIONS['ARM_1_SERVO'] + app.config['SERVO_DELTA'])
    elif command == 'arm1_lower':
        set_servo('ARM_1_SERVO', SERVO_POSITIONS['ARM_1_SERVO'] - app.config['SERVO_DELTA'])
    elif command == 'arm2_raise':
        set_servo('ARM_2_SERVO', SERVO_POSITIONS['ARM_2_SERVO'] - app.config['SERVO_DELTA'])
    elif command == 'arm2_lower':
        set_servo('ARM_2_SERVO', SERVO_POSITIONS['ARM_2_SERVO'] - app.config['SERVO_DELTA'])
    elif command == 'hand_grip':
        set_servo('GRIP_SERVO', SERVO_POSITIONS['GRIP_SERVO'] - app.config['SERVO_DELTA'])
    elif command == 'hand_release':
        set_servo('GRIP_SERVO', SERVO_POSITIONS['GRIP_SERVO'] - app.config['SERVO_DELTA'])
    else:
        logger.getLogger(__name__).error('Invalid command: %s' % command)

    return redirect(url_for('show_control'))


# Set servos to default position when app starts
set_servos_default()
