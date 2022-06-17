import feedparser
from bson.objectid import ObjectId

from GenericFeed.utils import db


class Feed:
    def __init__(self):
        self.collection = db.get_collection("feed")

    def check_feed(self, url):
        if self.collection.find_one({"url": url}):
            return True
        return False

    def add_feed(self, name: str, url: str):
        input_data = {"name": name, "url": url, "last_update": None}
        if self.check_feed(url):
            return False
        self.collection.insert_one(input_data)
        return True

    def remove_feed(self, id: str):
        deleted = self.collection.find_one_and_delete({"_id": ObjectId(id)})
        if deleted:
            return deleted
        return False

    def get_feeds(self):
        return self.collection.find()

    def get_feed(self, id: str):
        return self.collection.find_one({"_id": ObjectId(id)}, {"_id": 0})

    def update_feed(self, url):
        if self.check_feed(url):
            feed = feedparser.parse(url)
            self.collection.update_one(
                {"url": url}, {"$set": {"last_update": feed.entries[0].link}}
            )
            return True
        return False

    def check_update(self, url):
        if self.check_feed(url):
            feed = feedparser.parse(url)
            last_update = self.collection.find_one({"url": url})["last_update"]
            if last_update is None:
                return True
            try:
                return bool(feed.entries[0].link != last_update)
            except AttributeError:
                return False
        return False  # feed not found

    def clear_last_update(self, url):
        if self.check_feed(url):
            self.collection.update_one({"url": url}, {"$set": {"last_update": None}})
            return True
        return False
