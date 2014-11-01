import argparse
import logging
import os
import signal
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
        default='frame_%d.jpg',
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
        default=5.0,
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
        default=1024,
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


def get_image_filename_pattern(save_folder, filename_pattern):
    """
    Creates the save folders for timelapse recordings and returns the full image filename pattern.

    @param save_folder Folder in which to save all timelapse recordings
    @param filename_pattern Pattern for image filenames
    @returns filename pattern
    """

    logging.getLogger(__name__).debug('Getting filename pattern for images')
    logging.getLogger(__name__).debug('Save folder: %s. frame filename pattern: %s' % (save_folder, filename_pattern))

    folder_number = 0

    # If the folder already exists get the highest number and make the next folder one above that
    if os.path.exists(save_folder):
        sub_dirs = os.walk(save_folder).next()[1]
        for sub_dir in sub_dirs:
            try:
                sub_dir_number = int(sub_dir)
                if sub_dir_number > folder_number:
                    folder_number = sub_dir_number
            except ValueError:
                pass
        folder_number += 1

    # Make the folder for the current capture
    run_folder = os.path.join(save_folder, str(folder_number))
    logging.getLogger(__name__).debug('Making run folder: %s' % run_folder)
    os.makedirs(run_folder)

    # Get the filename pattern for the camera manager
    image_file_pattern = os.path.join(run_folder, filename_pattern)
    logging.getLogger(__name__).debug('Image file pattern: %s' % image_file_pattern)

    return image_file_pattern


GPS = None
TIMELAPSE = None


def stop_capture(signal_number, frame):
    """
    Stops capture and closes camera.

    @param signal_number Type of signal received
    @param frame Unused
    """

    logging.getLogger(__name__).info('Got signal %d, will exit' % signal_number)

    TIMELAPSE.stop()
    GPS.stop()


def start_capture(props):
    """
    Runs the timelapse capture.

    @param props Application properties
    """

    global GPS
    global TIMELAPSE

    logging.getLogger(__name__).info('Starting GPS...')
    host, port = props.gps.split(':')
    GPS = GPSHandler(host, port)
    GPS.start()

    logging.getLogger(__name__).info('Waiting for GPS fix...')
    while not GPS.has_fix():
        time.sleep(5)

    logging.getLogger(__name__).info('Setting up camera...')
    camera = CameraManager()
    camera.set_resolution(props.width, props.height)
    filename_pattern = get_image_filename_pattern(props.folder, props.filename)
    camera.set_filename_pattern(filename_pattern)

    logging.getLogger(__name__).info('Setting up timelapse...')
    TIMELAPSE = TimelapseWorkflow(camera, GPS)
    TIMELAPSE.set_interval(props.interval)
    TIMELAPSE.set_min_distance(props.distance)

    logging.getLogger(__name__).info('Starting timelapse')
    TIMELAPSE.start()

    # Register the signal handler used to stop capture
    signal.signal(signal.SIGINT, stop_capture)

    # Need this so that Python handles signals on the main thread
    while True:
        time.sleep(1)
