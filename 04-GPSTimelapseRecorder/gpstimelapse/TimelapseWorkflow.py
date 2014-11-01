import threading
import time


class TimelapseWorkflow(threading.Thread):
    """
    Manages the timelapse capture workflow.
    """

    def __init__(self, camera_manager, gps_manager):
        """
        Creates a new TimelapseWorkflow object.
        """

        threading.Thread.__init__(self)

        self._camera = camera_manager
        self._gps = gps_manager
        self._timer_interval = 1


    def set_timer_interval(self, interval):
        """
        Sets the interval for the timer.

        @param interval Time interval in seconds
        """

        if interval < 0.5:
            raise ValueError('Timer interval is too small to be useful')

        self._timer_interval = interval


    def run(self):
        """
        Main timer loop
        """

        while True:
            time.sleep(self._timer_interval)
            self._timer_handle()


    def _timer_handle(self):
        """
        Handles a timer tick.
        """

        # TODO
        # if gps_min and not gps_moved:
        #     return

        image_filename = self._camera.capture()

        self._post_process_image(image_filename)


    def _post_process_image(self, filename):
        """
        Performs post processing on an image (mainly adding EXIF tags.

        @param filename Image filename to process
        """

        # TODO
        pass
