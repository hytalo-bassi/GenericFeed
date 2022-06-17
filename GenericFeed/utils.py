from pyrogram.types import Message, CallbackQuery
from GenericFeed.config import DEV_LIST
from typing import Union
from pymongo import MongoClient
from GenericFeed.config import MONGODB_URI
from sys import exit


def is_sudoer(_, union: Union[Message, CallbackQuery]) -> bool:
    return union.from_user.id in DEV_LIST

if (MONGODB_URI is None):
    logging.error("The environment variable MONGODB_URI is not defined")
    exit(1)

db = MongoClient(MONGODB_URI).generic_feed

