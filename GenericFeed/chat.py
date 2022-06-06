# Chat manager for the GenericFeed bot
from GenericFeed.config import MONGODB_URI
from pymongo import MongoClient


class Chat:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client.get_database("generic_feed")
        self.chat = self.db.chat

    def check_chat(self, chat_id):
        if self.chat.find_one({"chat_id": chat_id}):
            return True
        else:
            return False

    def add_chat(self, chat_id, chat_name):
        if self.check_chat(chat_id):
            return False
        self.chat.insert_one({"chat_id": chat_id, "chat_name": chat_name})
        return True

    def remove_chat(self, chat_id):
        if not self.check_chat(chat_id):
            return False
        return self.chat.delete_one({"chat_id": chat_id})


    def get_chats(self):
        return self.chat.find()

    def get_chat(self, chat_id):
        return self.chat.find_one({"chat_id": chat_id})
