from AbstractWidget import AbstractWidget
import time


class DigitalClock(AbstractWidget):

    def get_data(self, config):
        data = dict()
        data['time'] = time.asctime()
        return data
