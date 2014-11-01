import logging
import threading
import time


class TimelapseWorkflow(threading.Thread):
    """
    Manages the timelapse capture workflow.
    """

    def __init__(self, camera_manager=None, gps_manager=None):
        """
        Creates a new TimelapseWorkflow object.
        """

        threading.Thread.__init__(self)

        self._camera = camera_manager
        self._gps = gps_manager

        self._run = True
        self._min_distance = None
        self._timer_interval = 1

        self._position = self._gps.get_position()


    def set_interval(self, interval):
        """
        Sets the interval for the timer.

        @param interval Time interval in seconds
        """

        if interval < 0.5:
            raise ValueError('Timer interval is too small to be useful')

        logging.getLogger(__name__).debug('TImer interval is now %f s' % interval)
        self._timer_interval = interval


    def set_min_distance(self, min_distance):
        """
        Sets the minumum distance that must be traveled between frames.

        Set to None to remove minimum distance restriction.

        @param min_distance Minimum distance in Km
        """

        if min_distance is not None and min_distance <= 0.0:
            raise ValueError('Minimum dtstance must be greater than 0')

        if min_distance is None:
            logging.getLogger(__name__).debug('Min GPS distance restriction removed')
        else:
            logging.getLogger(__name__).debug('Min GPS distance between frames is now %f Km' % min_distance)

        self._min_distance = min_distance


    def run(self):
        """
        Main timer loop
        """

        while self._run:
            logging.getLogger(__name__).debug('Timer has ticked')
            self._timer_handle()

            # Use 1 second timers to reduce time to wait on SIGINT
            for _ in range(0, int(self._timer_interval)):
                time.sleep(1)
                if not self._run:
                    return


    def stop(self):
        """
        Stops the current timelapse recording.
        """

        logging.getLogger(__name__).info('Stopping timelapse')
        self._run = False


    def _timer_handle(self):
        """
        Handles a timer tick.
        """

        delta_dist = self._gps.get_distance_from(self._position)
        logging.getLogger(__name__).debug('Distance moved since last capture is %f Km' % delta_dist)

        restrict_delta_dist = self._min_distance is not None
        delta_dist_over = delta_dist >= self._min_distance

        # If enforcing min distance between frames and we have not traveled further
        # the threshold then just return without cpaturing an image
        if restrict_delta_dist and not delta_dist_over:
            logging.getLogger(__name__).info('Have not moved far enough since last capture, will not capture a new frame yet')
            return

        # Capture a new frame
        image_filename = self._camera.capture()

        # Record the location the frame was captured
        self._position = self._gps.get_position()

        self._post_process_image(image_filename, self._position)


    def _post_process_image(self, filename, position):
        """
        Performs post processing on an image (mainly adding EXIF tags).

        @param filename Image filename to process
        @param position Location where the frame was captured
        """

        pass
