from AbstractWidget import AbstractWidget
import feedparser


class AbstractRSSFeed(AbstractWidget):

    def get_data(self, config):
        if 'feed_url' not in config:
            raise RuntimeError('Feed URL not set in config file')

        number_items = 10
        if 'num_items' in config:
            number_items = int(config['num_items'])
        self.logger.debug('Number of RSS items: %d' % number_items)

        feed_url = config['feed_url']
        self.logger.debug('RSS feed URL: %s' % feed_url)

        feed = feedparser.parse(feed_url)
        sorted_items = sorted(feed['items'], key=lambda entry: entry['published_parsed'])
        sorted_items.reverse()

        sorted_items = sorted_items[:number_items]
        items = list()

        for feed_item in sorted_items:
            item = dict()
            item['title'] = feed_item['title']
            item['summary'] = feed_item['summary']
            item['date'] = feed_item['published']

            items.append(item)

        data = { 'items':items }
        return data
