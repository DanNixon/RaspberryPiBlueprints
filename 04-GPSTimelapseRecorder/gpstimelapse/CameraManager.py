import logging
import time

import picamera


class CameraManager(object):
    """
    Handles capturing a sequence of still images.
    """

    def __init__(self):
        """
        Create a new camera manager.
        """

        self._filename_pattern = None
        self._current_capture_number = 0

        self._preview_time = 5

        self._camera = picamera.PiCamera()

        logging.getLogger(__name__).debug('Starting camera preview')
        self._camera.start_preview()


    def __del__(self):
        """
        Closes camera preview.
        """

        logging.getLogger(__name__).debug('Stopping camera preview')
        self._camera.stop_preview()


    def capture(self):
        """
        Captures a new image.

        @returns The filename the image will be saved to
        """

        logging.getLogger(__name__).info('Capturing new still image')

        filename = self._get_image_filename()
        self._current_capture_number += 1

        logging.getLogger(__name__).debug('Capturing image: %s' % filename)
        self._camera.capture(filename)

        return filename


    def set_filename_pattern(self, pattern):
        """
        Sets the fotmat pattern for image filenames.

        Must contain a %d indicating the frame/image number.

        @param pattern Filename pattern
        """

        self._filename_pattern = pattern


    def set_resolution(self, width, height):
        """
        Sets the image capture resolution.

        @param width Image width
        @param height Image height
        """

        self._camera.resolution = (width, height)


    def get_num_captures(self):
        """
        Gets the nunber of images captured.

        @returns Image count
        """

        return self._current_capture_number + 1


    def get_image_files(self):
        """
        Gets a list of filenames for every image captured.

        @returns List of filenames as strings
        """

        files = list()

        for idx in range(0, self._current_capture_number):
            filename = self._get_image_filename(idx)
            files.append(filename)

        return files


    def _get_image_filename(self, index=-1):
        """
        Gets the filename for a given index in the sequence.

        @param index Index of image (defaults to next to be captured)
        @returns Image filename
        """

        if index == -1:
            index = self._current_capture_number

        if self._filename_pattern is None:
            raise RuntimeError('No filename pattern has been set')

        filename = self._filename_pattern % index
        return filename
