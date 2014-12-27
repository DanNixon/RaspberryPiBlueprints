from AbstractWidget import AbstractWidget
import feedparser


class AbstractRSSFeed(AbstractWidget):

    def get_data(self, config):
        if 'feed_url' not in config:
            raise RuntimeError('Feed URL not set in config file')

        number_items = 10
        if 'num_items' in config:
            number_items = int(config['num_items'])

        feed = feedparser.parse(config['feed_url'])
        sorted_items = sorted(feed['items'], key=lambda entry: entry['published_parsed'])
        sorted_items.reverse()

        sorted_items = sorted_items[:10]
        items = list()

        for feed_item in sorted_items:
            item = dict()
            item['title'] = feed_item['title']
            item['summary'] = feed_item['summary']
            item['date'] = feed_item['published']

            items.append(item)

        data = { 'items':items }
        return data
