#!/usr/bin/python
import serial
import sqlite3
import time
from threading import Thread


# Variables to hold readings
RAIN_COUNTS = 0
WIND_SPEED_READINGS = list()
WIND_DIRECTION_READINGS = list()


SERIAL_PORT = None
SQLITE_DB_FILE = '/home/dan/RaspberryPi-Blueprints/06-WeatherStation/weather_station_webapp/weather.db'


def stop_sensor_recording():
    """
    """

    pass


def submit_reading_loop():
    """
    Submits the readings taken to the SQLite database.
    """

    global RAIN_COUNTS
    global WIND_SPEED_READINGS
    global WIND_DIRECTION_READINGS

    while True:
        avg_wind_speed = 0.0
        peak_wind_speed = 0.0
        for speed in WIND_SPEED_READINGS:
            if speed > peak_wind_speed:
                peak_wind_speed = speed
            avg_wind_speed += speed
        if len(WIND_SPEED_READINGS):
            avg_wind_speed /= len(WIND_SPEED_READINGS)

        connection = sqlite3.connect(SQLITE_DB_FILE)
        cursor = connection.cursor()
        sql = "INSERT INTO weather_history (wind_direction, average_wind_speed, peak_wind_speed, rain_frequency, temperature, humidity, pressure, light_level) VALUES ('%s', %f, %f, %f, %f, %f, %f, %f)" % ('North', avg_wind_speed, peak_wind_speed, RAIN_COUNTS, 0.0, 0.0, 0.0, 0.0)
        print sql
        cursor.execute(sql)
        connection.commit()
        connection.close()

        RAIN_COUNTS = 0
        WIND_SPEED_READINGS = list()
        WIND_DIRECTION_READINGS = list()

        time.sleep(10)


def poll_sensors():
    """
    Poll the sensors and take readings.
    """

    # Get new data from serial port form Maplin sensors
    response = SERIAL_PORT.readline()
    data = response.split(':')

    if data[0] == 'RAIN_DETECT':
        RAIN_COUNTS += 1;
    elif data[0] == 'WIND_DIRECTION':
        value = int(data[2].split(';')[0])
        WIND_DIRECTION_READINGS.append(value)
    elif data[0] == 'WIND_SPEED':
        value = float(data[2].split(';')[0])
        WIND_SPEED_READINGS.append(value)

    # TODO: Poll DHT sensor
    # TODO: Poll barometer


if __name__ == '__main__':
    # Serial port setup
    SERIAL_PORT = serial.Serial()
    SERIAL_PORT.port = "/dev/ttyACM0"
    SERIAL_PORT.baudrate = 115200
    SERIAL_PORT.timeout = 1

    try:
        SERIAL_PORT.open()
    except Exception, e:
        print "Error opening serial port: " + str(e)
        sys.exit(1)

    thread = Thread(target=submit_reading_loop)
    thread.start()

    # Loop to poll all sensors
    while True:
        try:
            poll_sensors()

        except Exception, e:
            print 'Sensor error: ' + str(e)
