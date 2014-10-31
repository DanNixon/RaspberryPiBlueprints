

def _haversine():
    pass


class GPSHandler(object):
    """
    Handles getting GPS data from gpsd and processing it.
    """

    def __init__(self):
        """
        """

        pass


    def get_position(self):
        """
        Gets the current GPS latitude and longitude.

        @returns Tuple of lat and lon
        """

        pass


    def get_delta_position_scalar(self, position):
        """
        Gets the distance between the current position and a given position
        as latitude and longitude in Km.

        @param position Other position
        @returns Distance difference
        """

        pass
