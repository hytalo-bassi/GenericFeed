from GenericFeed.utils import db


class LoopController:
    def __init__(self):
        self.collection = db.loop_controller

    def get_loop_status(self):
        return self.collection.find_one()["status"]

    def set_loop_status(self, status):
        self.collection.update_one({}, {"$set": {"status": status}}, upsert=True)
