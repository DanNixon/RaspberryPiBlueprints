from AbstractRSSFeed import AbstractRSSFeed


class RSSTicker(AbstractRSSFeed):

    def get_data(self, config):
        data = AbstractRSSFeed.get_data(self, config)

        text_type = config.get('text_type', 'title')
        data['update_time'] = config.get('ticker_update_time', 5)

        new_items = [item[text_type] for item in data['items']]
        data['items'] = new_items

        return data
