from AbstractWidget import AbstractWidget
from ConfigParser import NoOptionError
from pytz import timezone
from datetime import datetime


class AbstractClock(AbstractWidget):

    def get_data(self, config):
        try:
            user_timesone = config.get('widget', 'timezone')
            time_zone = timezone(user_timesone)
            self.logger.info('Get timezone form config file: %s' % str(time_zone))
            current_time = datetime.now(time_zone)

        except NoOptionError:
            current_time = datetime.now()

        data = dict()
        data['year'] = current_time.year
        data['month'] = current_time.month
        data['day'] = current_time.day
        data['hour'] = current_time.hour
        data['minute'] = current_time.minute
        data['second'] = current_time.second

        return data
