import time
import thread

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


    def capture(self):
        """
        Captures a new image.
        """

        filename = self._get_image_filename()
        self._current_capture_number += 1

        thread.start_new_thread(self._capture_routine, (filename))


    def _capture_routine(self, filename):
        """
        Handles the camera preview and image capture.

        @param filename Filename to save as
        """

        self._camera.start_preview()

        time.sleep(self._preview_time)
        self._camera.capture(filename)

        self._camera.stop_preview()


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


    def _get_image_filename(self, index = -1):
        """
        Gets the filename for a given index in the sequence.

        @param index Index of image (defaults to next to be captured)
        @returns Image filename
        """

        if index == -1:
            index = self._current_cature_number

        if self._filename_pattern is None:
            raise RuntimeError('No filename pattern has been set')

        filename = self._filename_pattern % index
        return filename
