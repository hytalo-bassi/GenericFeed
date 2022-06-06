from pyrogram.types import Message, CallbackQuery
from GenericFeed.config import DEV_LIST
from typing import Union


def is_sudoer(_, union: Union[Message, CallbackQuery]) -> bool:
    return union.from_user.id in DEV_LIST
