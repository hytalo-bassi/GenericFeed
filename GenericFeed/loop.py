from pymongo import MongoClient
from GenericFeed.config import MONGODB_URI

mongodb_client = MongoClient(MONGODB_URI)


class LoopController:
    def __init__(self):
        self.db = mongodb_client.loop_controller
        self.collection = self.db.loop_controller

    def get_loop_status(self):
        return self.collection.find_one()["status"]

    def set_loop_status(self, status):
        self.collection.update_one({}, {"$set": {"status": status}}, upsert=True)
