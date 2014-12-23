from AbstractWidget import AbstractWidget
from ConfigParser import NoOptionError
from pytz import timezone
import datetime, time


class Clock(AbstractWidget):

    def get_data(self, config):
        try:
            user_timesone = config.get('widget', 'zone')
            time_zone = timezone(user_timesone)
            current_time = datetime.now(time_zone)

        except NoOptionError:
            current_time = time.localtime()

        data = dict()
        data['year'] = current_time.tm_year
        data['month'] = current_time.tm_mon
        data['day'] = current_time.tm_mday
        data['hour'] = current_time.tm_hour
        data['minute'] = current_time.tm_min
        data['second'] = current_time.tm_sec

        return data
