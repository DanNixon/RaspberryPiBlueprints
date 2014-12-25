from AbstractWidget import AbstractWidget
from ConfigParser import NoOptionError
from pytz import timezone
from datetime import datetime
from calendar import timegm


class AbstractClock(AbstractWidget):

    def get_data(self, config):
        data = dict()

        try:
            user_timezone = config.get('widget', 'timezone')
            time_zone = timezone(user_timezone)
            data['timezone'] = time_zone.zone
            self.logger.info('Get timezone form config file: %s' % str(time_zone))
            current_time = datetime.now(time_zone)

        except NoOptionError:
            data['timezone'] = 'System Time'
            current_time = datetime.now()

        data['year'] = current_time.year
        data['month'] = current_time.month
        data['day'] = current_time.day
        data['hour'] = current_time.hour
        data['minute'] = current_time.minute
        data['second'] = current_time.second

        data['epoch_seconds'] = timegm(current_time.timetuple())

        return data
