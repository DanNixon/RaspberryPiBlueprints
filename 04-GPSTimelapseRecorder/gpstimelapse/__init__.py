import argparse
import logging
import sys
import time

from gpstimelapse.CameraManager import CameraManager
from gpstimelapse.GPSHandler import GPSHandler
from gpstimelapse.TimelapseWorkflow import TimelapseWorkflow


def run():
    """
    Gets command line options and starts timelapse recorder.
    """
    parser = argparse.ArgumentParser(description='GPS enabled timelapse recorder')

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Increases console verbosity'
    )

    parser.add_argument(
        '--gps',
        action='store',
        default='localhost:2947',
        help='Specifies address to connect to cgps daemon (default localhost::2947)'
    )

    parser.add_argument(
        '-f', '--folder',
        action='store',
        default='~/timelapse_recordings/',
        help='Specifies folder to save timelapse recordings in'
    )

    parser.add_argument(
        '-n', '--filename',
        action='store',
        default='%N_%T_%n.jpg',
        help='Filename pattern for image files'
    )

    parser.add_argument(
        '-d', '--distance',
        action='store',
        type=float,
        help='Distance in meters to have moved between captures'
    )

    parser.add_argument(
        '-i', '--interval',
        action='store',
        type=float,
        help='Time in seconds between captures'
    )

    parser.add_argument(
        '--width',
        action='store',
        type=int,
        default=1248,
        help='Height of captured images'
    )

    parser.add_argument(
        '--height',
        action='store',
        type=int,
        default=1024
        help='Width of captured images'
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
    logging.getLogger(__name__).info('Got parameters, will start timelapse')

    start_capture(props)


def start_capture(props):
    """
    Runs the timelapse capture.

    @param props Application properties
    """

    logging.getLogger(__name__).info('Starting GPS...')
    host, port = props.gps.split(':')
    gps = GPSHandler(host, port)
    gps.start()

    # TODO: wait for GPS lock

    logging.getLogger(__name__).info('Setting up camera...')
    camera = CameraManager()
    camera.set_resolution(props.width, props.height)
    camera.set_filename_pattern(props.filename)

    logging.getLogger(__name__).info('Setting up timelapse...')
    timelapse = TimelapseWorkflow(camera, gps)
    timelapse.set_interval(props.interval)
    timelapse.set_min_distance(props.distance)

    logging.getLogger(__name__).info('Starting timelapse')
    timelapse.start()
