# Chat manager for the GenericFeed bot
from GenericFeed.utils import db


class Chat:
    def __init__(self):
        self.chat = db.chat

    def check_chat(self, chat_id):
        if self.chat.find_one({"chat_id": chat_id}):
            return True
        return False

    def add_chat(self, chat_id, chat_name):
        if self.check_chat(chat_id):
            return False
        self.chat.insert_one({"chat_id": chat_id, "chat_name": chat_name})
        return True

    def remove_chat(self, chat_id: int):
        if not self.check_chat(chat_id):
            return False
        self.chat.delete_one({"chat_id": chat_id})
        return True

    def get_chats(self):
        return self.chat.find()

    def get_chat(self, chat_id):
        return self.chat.find_one({"chat_id": chat_id})
