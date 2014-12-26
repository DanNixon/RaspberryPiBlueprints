from AbstractWidget import AbstractWidget
import requests


class Weather(AbstractWidget):

    _api_url_root = 'http://api.openweathermap.org/data/2.5/'


    def get_data(self, config):
        request_params = { 'q':'London, UK', 'units':'metric' }
        # TODO: set params

        # Get data from OpenWeatherMap API
        service_url = self._api_url_root + 'weather'
        api_request = requests.get(service_url, params=request_params)
        api_data = api_request.json()

        # Format data into our response format
        data = dict()

        data['units'] = request_params['units']
        data['location_name'] = api_data['name']
        data['humidity'] = api_data['main']['humidity']
        data['pressure'] = api_data['main']['pressure']

        data['temperature'] = {
            'current':api_data['main']['temp'],
            'min':api_data['main']['temp_min'],
            'max':api_data['main']['temp_max'] }

        data['wind'] = {
            'speed':api_data['main']['temp'],
            'direction':api_data['wind']['deg'],
            'direction_name': self._degrees_to_compass(api_data['wind']['deg']) }

        data['current'] = {
            'icon':self._get_icon_url(api_data['weather'][0]['icon']),
            'name':api_data['weather'][0]['main'],
            'description': api_data['weather'][0]['description'] }

        return data


    def _get_icon_url(self, icon):
        """
        Gets the URL for an icon from OpenWeatherMap.

        @param icon Icon ID
        @return URL for icon image
        """

        url_format = 'http://openweathermap.org/img/w/%s.png'
        url = url_format % icon

        self.logger.debug('Got icon URL for icon %s: %s' % (icon, url))

        return url


    def _degrees_to_compass(self, degrees):
        """
        Converts a direction in degrees to a compass direction (out of 8 possible).

        @param degrees Direction in degrees
        @return Name of compass direction
        """

        # Get the parameter in the correct format
        if type(degrees) is not float:
            degrees = float(degrees)

        # Use a lambda for range comparison
        between = lambda a, b: degrees >= a and degrees < b

        directions = {
            'north':0,
            'north east':45,
            'east':90,
            'south east':135,
            'south':180,
            'south west':225,
            'west':270,
            'north west':315
            }

        half_direction_range = 180.0 / len(directions)

        for name, centre in directions.items():
            # Calculate upper and lower ranges
            lower = centre - half_direction_range
            upper = centre + half_direction_range

            # Correct lower when it goes negative
            if lower < 0:
                lower += 360.0

            self.logger.debug('Direction %s from %d to %d' % (name, lower, upper))

            # If within ranges return the direction name
            if between(lower, upper):
                return name

        # Should never happen
        return ''
