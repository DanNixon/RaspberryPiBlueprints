#!/usr/bin/python
import Adafruit_DHT
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
TEMPERATURE_READINGS = list()
HUMIDITY_READINGS = list()
PRESSURE_READINGS = list()

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
    global TEMPERATURE_READINGS
    global HUMIDITY_READINGS
    global PRESSURE_READINGS

    while RUN:
        time.sleep(interval)

        try:
            # Get average values
            avg_wind_speed, peak_wind_speed = get_stats(WIND_SPEED_READINGS)
            average_light_level = get_stats(LIGHT_LEVEL_READINGS)[0]
            average_temperature = get_stats(TEMPERATURE_READINGS)[0]
            average_humidity = get_stats(HUMIDITY_READINGS)[0]
            average_pressure = get_stats(PRESSURE_READINGS)[0]

            # Get modal wind direction
            directions = Counter(WIND_DIRECTION_READINGS)
            modal_directions = directions.most_common(1)
            modal_direction = -1
            if len(modal_directions) > 0:
                modal_direction = modal_directions[0][0]
            logging.getLogger(__name__).debug('Wind direction: %d' % modal_direction)

            connection = sqlite3.connect(database)
            cursor = connection.cursor()
            sql = "INSERT INTO weather_history (wind_direction, average_wind_speed, peak_wind_speed, rain_frequency, temperature, humidity, pressure, light_level) VALUES ('%s', %f, %f, %f, %f, %f, %f, %f)" % (DIRECTION_ID_TO_NAME[modal_direction], avg_wind_speed, peak_wind_speed, RAIN_COUNTS, average_temperature, average_humidity, average_pressure, average_light_level)
            logging.getLogger(__name__).debug('SQL statement: ' + sql)
            cursor.execute(sql)
            connection.commit()
            connection.close()

            SERIAL_PORT.write('D\r\n')

        except Exception as e:
            print 'Error submitting readings: ' + str(e)

        RAIN_COUNTS = 0
        WIND_SPEED_READINGS = list()
        WIND_DIRECTION_READINGS = list()
        LIGHT_LEVEL_READINGS = list()


def get_stats(data):
    """
    Finds the mean and peak values for data in a list.

    @param data Data to get statistics for
    """
    average = 0.0
    peak = 0.0

    for value in data:
        if value > peak:
            peak = value
        average += value

    if len(data):
        average /= len(data)

    return average, peak


def poll_serial_sensors():
    """
    Poll the sensors on the serial port and take readings.
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


def poll_gpio_sensors_loop(interval):
    """
    Poll the sensors on the serial port and take readings.

    @param interval TIme to wait between polling
    """

    while RUN:
        # Get temperature and humidity from DHT sensor
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
        TEMPERATURE_READINGS.append(temperature)
        HUMIDITY_READINGS.append(humidity)

        # TODO: Poll barometer

        time.sleep(interval)


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
    SERIAL_PORT.timeout = 1

    try:
        SERIAL_PORT.open()
    except Exception, e:
        logging.getLogger(__name__).error('Error opening serial port: ' + str(e))
        sys.exit(1)

    db_submit_loop = Thread(target=submit_reading_loop, args=(params.database, params.submit_interval))
    db_submit_loop.start()

    gpio_poll_loop = Thread(target=poll_gpio_sensors_loop, args=(params.poll_interval,))
    gpio_poll_loop.start()

    # Loop to poll serial port
    while RUN:
        try:
            poll_serial_sensors()
        except Exception, e:
            logging.getLogger(__name__).error('Serial sensor error: ' + str(e))

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
        default='weather_sensors.log',
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
