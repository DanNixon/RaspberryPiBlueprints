from AbstractWidget import AbstractWidget

from TwitterSearch import *


class TwitterSearchFeed(AbstractWidget):

    def get_data(self, config):
        count = int(config.get('count', 50))

        # Configure the search query
        tso = TwitterSearchOrder()
        tso.set_keywords([config['query']])
        tso.set_include_entities(False)

        # Configure the search
        ts = TwitterSearch(
               consumer_key=config['consumer_key'],
               consumer_secret=config['consumer_secret'],
               access_token=config['access_token'],
               access_token_secret=config['access_secret']
               )

        data = dict()
        data['query'] = config['query']
        data['tweets'] = list()

        # Do the search
        result = ts.search_tweets(tso)['content']['statuses']

        # Filter results into more usable format
        for tweet in result[:count]:
            filtered_tweet = dict()
            filtered_tweet['username'] = '@' + tweet['user']['screen_name']
            filtered_tweet['tweet'] = tweet['text']
            data['tweets'].append(filtered_tweet)

        return data
