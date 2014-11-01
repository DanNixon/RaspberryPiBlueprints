import logging
import threading
import time

import gps


def _haversine(pos_a, pos_b):
    """
    Calculates the distance between two GPS points as decimal latitude and longitude.

    @param pos_a First position tuple
    @param pos_b Second position tuple
    @returns Distance between points in Km
    """

    logging.getLogger('haversine').debug('Calculating distance between points')
    logging.getLogger('haversine').debug('First: %s, second %s' % (str(pos_a), str(pos_b)))

    degree_to_rad = float(pi / 180.0)

    delta_lat = (pos_b[0] - pos_a[0]) * degree_to_rad
    delta_lon = (pos_b[1] - pos_b[1]) * degree_to_rad

    a = pow(sin(delta_lat / 2), 2) + cos(pos_a[0] * degree_to_rad) * cos(pos_b[1] * degree_to_rad) * pow(sin(delta_lon / 2), 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    delta_km = 6367 * c

    logging.getLogger('haversine').debug('Got delta distance: %f Km' % delta_km)

    return delta_km


class GPSHandler(threading.Thread):
    """
    Handles getting GPS data from gpsd and processing it.
    """

    def __init__(self, host='localhost', port=2947):
        """
        Creates a new GPS handler to connect to a given GPSD instance.

        @param host The host of the GPSD instance to connect to (defaults to localhost)
        @param port The port to connect on (defaults to 2947)
        """

        threading.Thread.__init__(self)

        self._current_report = None

        logging.getLogger(__name__).info('Connecting to GPSD on host: %s, port %s'
                                         % (host, str(port)))

        self._gps = gps.gps(host, port)
        self._gps.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)


    def run(self):
        """
        Polls GPS daemon for new position data.
        """

        try:
            while True:
                # Get a new report from GPSD
                report = self._gps.next()

                # TPV reports are the ones we are interested in, they contain fix and location data
                if report['class'] == 'TPV':
                    logging.getLogger(__name__).info('Got new GPS TPV report')
                    self._current_report = report

            # Check for reports at a reasonable rate
            time.sleep(1)

        except StopIteration:
            pass


    def has_fix(self):
        """
        Tests if there is a current GPS fix

        @returns True if GPS has fix
        """

        if self._current_report is None:
            raise RuntimeError('No report received yet')

        try:
            fix = self._current_report['mode'] == 3
        except IndexError:
            fix = False

        logging.getLogger(__name__).debug('has_fix: %s' % str(fix))

        return fix


    def get_position(self):
        """
        Gets the current GPS latitude and longitude.

        @returns Tuple of lat and lon
        """

        if not self.has_fix():
            raise RuntimeError('No GPS fix')

        if self._current_report is None:
            raise RuntimeError('No report received yet')

        position = (self._current_report['lat'], self._current_report['lon'])
        return position


    def get_delta_position_scalar(self, position):
        """
        Gets the distance between the current position and a given position
        as latitude and longitude in Km.

        @param position Other position tuple
        @returns Distance difference
        """

        current_position = self.get_position()
        delta_km = _haversine(current_position, position)
        return delta_km
