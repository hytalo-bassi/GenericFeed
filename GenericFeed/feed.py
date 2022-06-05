import feedparser
from pymongo import MongoClient
from GenericFeed.config import MONGODB_URI


class Feed:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client.get_database('generic_feed')
        self.collection = self.db.get_collection('feed')

    def check_feed(self, url):
        if self.collection.find_one({'url': url}):
            return True
        else:
            return False

    def add_feed(self, name: str, url: str):
        input_data = {
            'name': name,
            'url': url,
            'last_update': None
        }
        if self.check_feed(url):
            return False
        else:
            self.collection.insert_one(input_data)
            return True

    def remove_feed(self, url):
        if self.check_feed(url):
            self.collection.delete_one({'url': url})
            return True
        else:
            return False

    def get_feeds(self):
        return self.collection.find({}, {'_id': 0})

    def get_feed(self, url):
        return self.collection.find_one({'url': url}, {'_id': 0})

    def update_feed(self, url):
        if self.check_feed(url):
            feed = feedparser.parse(url)
            self.collection.update_one(
                {'url': url},
                {'$set': {'last_update': feed.entries[0].link}}
            )
            return True
        else:
            return False

    def check_update(self, url):
        if self.check_feed(url):
            feed = feedparser.parse(url)
            last_update = self.collection.find_one({'url': url})['last_update']
            if last_update is None:
                return True
            else:
                if feed.entries[0].link != last_update:
                    return True     # new update
                else:
                    return False    # No update
        else:
            return False    # feed not found
