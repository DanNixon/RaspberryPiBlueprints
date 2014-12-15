# -*- coding: utf-8 -*-
"""
Web application to control servos for a robot arm via RPi GPIO.
"""

import os, logging
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template
import RPIO
from RPIO import PWM


app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,

    LOG_FILE='robot_arm.log',
    LOG_LEVEL='DEBUG',

    SERVO_DELTA=50,

    ARM_1_A_SERVO_GPIO=None,
    ARM_1_B_SERVO_GPIO=None,
    ARM_2_SERVO_GPIO=None,
    GRIP_SERVO_GPIO=None,

    ARM_1_A_SERVO_MIN=600,
    ARM_1_B_SERVO_MIN=600,
    ARM_2_SERVO_MIN=600,
    GRIP_SERVO_MIN=600,

    ARM_1_A_SERVO_MAX=2500,
    ARM_1_B_SERVO_MAX=2500,
    ARM_2_SERVO_MAX=2500,
    GRIP_SERVO_MAX=2500,

    MOTOR_POWER_GPIO=None,
    MOTOR_1_A_GPIO=None,
    MOTOR_1_B_GPIO=None,
    MOTOR_2_A_GPIO=None,
    MOTOR_2_B_GPIO=None
))
app.config.from_envvar('ROBOT_ARM_SETTINGS', silent=False)


log_level = getattr(logging, app.config['LOG_LEVEL'].upper(), None)
logging.basicConfig(level=log_level, filename=app.config['LOG_FILE'])

SERVO_POSITIONS = dict()
SERVOS = dict()

RPIO.setup(app.config['MOTOR_1_A_GPIO'], RPIO.OUT, initial=RPIO.HIGH)
RPIO.setup(app.config['MOTOR_1_B_GPIO'], RPIO.OUT, initial=RPIO.HIGH)
RPIO.setup(app.config['MOTOR_2_A_GPIO'], RPIO.OUT, initial=RPIO.HIGH)
RPIO.setup(app.config['MOTOR_2_B_GPIO'], RPIO.OUT, initial=RPIO.HIGH)
RPIO.setup(app.config['MOTOR_POWER_GPIO'], RPIO.OUT, initial=RPIO.HIGH)


def set_servo(servo_id, position):
    """
    Sets a given GPIO.

    @param servo_id ID of servo to set
    @param position Timing value for servo position, will be rounded to nearest 10us
    """

    max_pos = app.config[servo_id + '_MAX']
    min_pos = app.config[servo_id + '_MIN']

    # Ignore positions out of the valid range
    if position > max_pos:
        logging.getLogger(__name__).error('Servo %s, position %d is greater than max %d' % (servo_id, position, max_pos))
        return
    if position < min_pos:
        logging.getLogger(__name__).error('Servo %s, position %d is less than min %d' % (servo_id, position, min_pos))
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


def set_base_movement(movement_type):
    """
    Sets a base movement type on the motor outputs.

    @param movement_type Movement command.
    """

    if movement_type == 'mov_fwd':
        RPIO.output(app.config['MOTOR_1_A_GPIO'], False)
        RPIO.output(app.config['MOTOR_1_B_GPIO'], True)
        RPIO.output(app.config['MOTOR_2_A_GPIO'], False)
        RPIO.output(app.config['MOTOR_2_B_GPIO'], True)
    elif movement_type == 'mov_rev':
        RPIO.output(app.config['MOTOR_1_A_GPIO'], True)
        RPIO.output(app.config['MOTOR_1_B_GPIO'], False)
        RPIO.output(app.config['MOTOR_2_A_GPIO'], True)
        RPIO.output(app.config['MOTOR_2_B_GPIO'], False)
    elif movement_type == 'rot_cw':
        RPIO.output(app.config['MOTOR_1_A_GPIO'], False)
        RPIO.output(app.config['MOTOR_1_B_GPIO'], True)
        RPIO.output(app.config['MOTOR_2_A_GPIO'], True)
        RPIO.output(app.config['MOTOR_2_B_GPIO'], False)
    elif movement_type == 'rot_ccw':
        RPIO.output(app.config['MOTOR_1_A_GPIO'], True)
        RPIO.output(app.config['MOTOR_1_B_GPIO'], False)
        RPIO.output(app.config['MOTOR_2_A_GPIO'], False)
        RPIO.output(app.config['MOTOR_2_B_GPIO'], True)
    elif movement_type == 'stop':
        pass
    else:
        logging.getLogger(__name__).error('Unknown movement type: %s' % movement_type)

    power = movement_type != 'stop'
    logging.getLogger(__name__).debug('Setting motor power: %s' % str(power))
    RPIO.output(app.config['MOTOR_POWER_GPIO'], not power)


def set_servos_default():
    """
    Sets all servos to their default position.
    """
    logging.getLogger(__name__).info('Resetting servos to default position')
    all_servo_ids = ['ARM_1_A_SERVO', 'ARM_1_B_SERVO', 'ARM_2_SERVO', 'GRIP_SERVO']
    for servo_id in all_servo_ids:
        set_servo(servo_id, app.config[servo_id + '_MIN'])

    logging.getLogger(__name__).info('Enabling motor power')


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
    """
    Handles a command from the web UI.

    @param command Command sent to web API
    """

    logging.getLogger(__name__).debug('Got command: %s' % command)

    base_movement_commands = ['mov_fwd', 'mov_rev', 'rot_cw', 'rot_ccw', 'stop']

    if command in base_movement_commands:
        set_base_movement(command)
    elif command == 'arm1_raise':
        set_servo('ARM_1_A_SERVO', SERVO_POSITIONS['ARM_1_A_SERVO'] + app.config['SERVO_DELTA'])
        set_servo('ARM_1_B_SERVO', SERVO_POSITIONS['ARM_1_B_SERVO'] + app.config['SERVO_DELTA'])
    elif command == 'arm1_lower':
        set_servo('ARM_1_A_SERVO', SERVO_POSITIONS['ARM_1_A_SERVO'] - app.config['SERVO_DELTA'])
        set_servo('ARM_1_B_SERVO', SERVO_POSITIONS['ARM_1_B_SERVO'] - app.config['SERVO_DELTA'])
    elif command == 'arm2_raise':
        set_servo('ARM_2_SERVO', SERVO_POSITIONS['ARM_2_SERVO'] + app.config['SERVO_DELTA'])
    elif command == 'arm2_lower':
        set_servo('ARM_2_SERVO', SERVO_POSITIONS['ARM_2_SERVO'] - app.config['SERVO_DELTA'])
    elif command == 'hand_grip':
        set_servo('GRIP_SERVO', SERVO_POSITIONS['GRIP_SERVO'] + app.config['SERVO_DELTA'])
    elif command == 'hand_release':
        set_servo('GRIP_SERVO', SERVO_POSITIONS['GRIP_SERVO'] - app.config['SERVO_DELTA'])
    else:
        logger.getLogger(__name__).error('Invalid command: %s' % command)

    return redirect(url_for('show_control'))


# Set servos to default position and base motors when app starts
set_servos_default()
set_base_movement('stop')
