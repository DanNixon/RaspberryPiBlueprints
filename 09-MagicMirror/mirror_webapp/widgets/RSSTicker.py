from AbstractRSSFeed import AbstractRSSFeed


class RSSTicker(AbstractRSSFeed):

    def get_data(self, config):
        data = AbstractRSSFeed.get_data(self, config)
        return data
