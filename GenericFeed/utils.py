import logging
import sys
from typing import Union

from pymongo import MongoClient
from pyrogram.types import CallbackQuery, Message

from GenericFeed.config import DEV_LIST, MONGODB_URI


def is_sudoer(_, union: Union[Message, CallbackQuery]) -> bool:
    return union.from_user.id in DEV_LIST


if MONGODB_URI is None:
    logging.error("The environment variable MONGODB_URI is not defined")
    sys.exit(1)

db = MongoClient(MONGODB_URI).generic_feed
