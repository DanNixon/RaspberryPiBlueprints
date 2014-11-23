#!/usr/bin/python
import argparse
from collections import Counter
import logging
import signal
import serial
import sqlite3
import sys
import time
from threading import Thread


# Variables to hold readings
RAIN_COUNTS = 0
WIND_SPEED_READINGS = list()
WIND_DIRECTION_READINGS = list()
LIGHT_LEVEL_READINGS = list()

RUN = True
SERIAL_PORT = None


DIRECTION_ID_TO_NAME = {
        -1 : 'Unknown',
        0 : 'North',
        1 : 'North East',
        2 : 'East',
        3 : 'South East',
        4 : 'South',
        5 : 'South West',
        6 : 'West',
        7 : 'North West',
    }


def stop_sensor_recording(signal_number, frame):
    """
    Stops data recording.

    @param signal_number Type of signal received
    @param frame Unused
    """

    global RUN
    RUN = False


def submit_reading_loop(database, interval):
    """
    Submits the readings taken to the SQLite database.

    @param database Database file to submit to
    @param interval Time interval in seconds to wait between submission
    """

    global RAIN_COUNTS
    global WIND_SPEED_READINGS
    global WIND_DIRECTION_READINGS
    global LIGHT_LEVEL_READINGS

    while RUN:
        time.sleep(interval)

        try:
            # Get avergae and peak wind speeds
            avg_wind_speed = 0.0
            peak_wind_speed = 0.0
            for speed in WIND_SPEED_READINGS:
                if speed > peak_wind_speed:
                    peak_wind_speed = speed
                avg_wind_speed += speed
            if len(WIND_SPEED_READINGS):
                avg_wind_speed /= len(WIND_SPEED_READINGS)
            logging.getLogger(__name__).debug('Average wind speed: %d' % avg_wind_speed)
            logging.getLogger(__name__).debug('Peak wind speed: %d' % peak_wind_speed)

            # Get modal wind direction
            directions = Counter(WIND_DIRECTION_READINGS)
            modal_directions = directions.most_common(1)
            modal_direction = -1
            if len(modal_directions) > 0:
                modal_direction = modal_directions[0][0]
            logging.getLogger(__name__).debug('Wind direction: %d' % modal_direction)

            # Get avaerage light level
            average_light_level = 0
            if len(LIGHT_LEVEL_READINGS) > 0:
                average_light_level = sum(LIGHT_LEVEL_READINGS) / len(LIGHT_LEVEL_READINGS)

            connection = sqlite3.connect(database)
            cursor = connection.cursor()
            sql = "INSERT INTO weather_history (wind_direction, average_wind_speed, peak_wind_speed, rain_frequency, temperature, humidity, pressure, light_level) VALUES ('%s', %f, %f, %f, %f, %f, %f, %f)" % (DIRECTION_ID_TO_NAME[modal_direction], avg_wind_speed, peak_wind_speed, RAIN_COUNTS, 0.0, 0.0, 0.0, average_light_level)
            logging.getLogger(__name__).debug('SQL statement: ' + sql)
            cursor.execute(sql)
            connection.commit()
            connection.close()

        except Exception as e:
            print 'Error submitting readings: ' + str(e)

        RAIN_COUNTS = 0
        WIND_SPEED_READINGS = list()
        WIND_DIRECTION_READINGS = list()
        LIGHT_LEVEL_READINGS = list()


def poll_sensors():
    """
    Poll the sensors and take readings.
    """

    # Get new data from serial port form Maplin sensors
    response = SERIAL_PORT.readline()
    data = response.split(':')

    if data[0].split(';')[0] == 'RAIN_DETECT':
        global RAIN_COUNTS
        RAIN_COUNTS += 1;
    elif data[0] == 'WIND_DIRECTION':
        value = int(data[2].split(';')[0])
        WIND_DIRECTION_READINGS.append(value)
    elif data[0] == 'LIGHT_LEVEL':
        value = int(data[2].split(';')[0])
        LIGHT_LEVEL_READINGS.append(value)
    elif data[0] == 'WIND_SPEED':
        value = float(data[2].split(';')[0])
        WIND_SPEED_READINGS.append(value)

    # TODO: Poll DHT sensor
    # TODO: Poll barometer


def start_sensor_recording(params):
    """
    Runs data capture script.

    @param params Options
    """

    # Serial port setup
    global SERIAL_PORT
    SERIAL_PORT = serial.Serial()
    SERIAL_PORT.port = params.serial_port
    SERIAL_PORT.baudrate = params.serial_baud
    SERIAL_PORT.timeout = params.poll_interval

    try:
        SERIAL_PORT.open()
    except Exception, e:
        logging.getLogger(__name__).error('Error opening serial port: ' + str(e))
        sys.exit(1)

    thread = Thread(target=submit_reading_loop, args=(params.database, params.submit_interval))
    thread.start()

    # Loop to poll all sensors
    while RUN:
        try:
            poll_sensors()

        except Exception, e:
            logging.getLogger(__name__).error('Sensor error: ' + str(e))

    sys.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Weather sensor client script')

    parser.add_argument(
        '--database',
        action='store',
        default='weather.db',
        help='Filename and path to the database file to write to'
    )

    parser.add_argument(
        '--serial-port',
        action='store',
        default='/dev/ttyACM0',
        help='Path to the serial port to use'
    )

    parser.add_argument(
        '--serial-baud',
        action='store',
        default=115200,
        help='Serial baud rate to use'
    )

    parser.add_argument(
        '--submit-interval',
        action='store',
        default=600,
        type=int,
        help='Time in seconds between data averaging and database submission'
    )

    parser.add_argument(
        '--poll-interval',
        action='store',
        default=10,
        type=int,
        help='Time in seconds between the sensors being polled'
    )

    parser.add_argument(
        '--log-file',
        action='store',
        default='gps_timelapse.log',
        help='File to save log to'
    )

    parser.add_argument(
        '--log-level',
        action='store',
        default='INFO',
        help='Logging level [DEBUG,INFO,WARNING,ERROR,CRITICAL]'
    )

    props = parser.parse_args()

    log_level = getattr(logging, props.log_level.upper(), None)
    if not isinstance(log_level, int):
        log_level = logging.INFO

    logging.basicConfig(level=log_level, filename=props.log_file)
    logging.getLogger(__name__).info('Starting recording')

    # Add a handler to stop recording on SIGINT (Ctrl-C)
    signal.signal(signal.SIGINT, stop_sensor_recording)

    start_sensor_recording(props)
