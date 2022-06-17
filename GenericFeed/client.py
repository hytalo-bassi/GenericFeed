import asyncio
import logging

from bs4 import BeautifulSoup as bs
from pyrogram import Client
from pyrogram.errors import (
    ChannelPrivate,
    ChatIdInvalid,
    PeerIdInvalid,
    UserIsBlocked,
    UserIsBot,
)

from GenericFeed.chat import Chat
from GenericFeed.config import FEED_FORMATTER_TEMPLATE


class GenericFeed(Client): # pylint: disable=too-many-ancestors
    def __init__(self, API_ID, API_HASH, BOT_TOKEN, workers: int = 4):
        super().__init__(
            "GenericFeed",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=workers,
            plugins=dict(root="GenericFeed/plugins"),
        )

    async def send_feed(self, chat_info, feed_data, limit: int = None):
        chat_id = chat_info["chat_id"]
        last_entry = feed_data["entries"][0]
        text_content = None
        image_content = None
        try:
            text_content = last_entry.summary

        except AttributeError:
            try:
                text_content = last_entry.description
            except AttributeError:
                text_content = "No description"

        if limit is not None:
            logging.info(f"Feed limited to {limit}")
            text_content = text_content[:limit] + "..."

        text_content = bs(text_content, "lxml").text  # Remove HTML tags
        try:
            image_content = last_entry["media_content"][0]["url"]

        except Exception:
            try:
                image_content = last_entry["image"]
            except Exception:
                logging.error("Can not load image")
            image_content = None

        formatted_text = FEED_FORMATTER_TEMPLATE.format(
            feed_title=feed_data["feed"]["title"],
            title=last_entry.title,
            url=last_entry.link,
            summary=(text_content if len(text_content) >= 0 else "No description."),
        )

        try:
            if image_content:
                await self.send_photo(
                    chat_id=chat_id,
                    photo=image_content,
                    caption=formatted_text,
                )
            else:
                await self.send_message(
                    chat_id=chat_id,
                    text=formatted_text,
                )
        except (
            ChatIdInvalid,
            PeerIdInvalid,
            ChannelPrivate,
            UserIsBlocked,
            UserIsBot,
        ) as err:
            logging.error(f"Can not send message to {chat_id}, removing fromn DB. Error: {err}")
            Chat().remove_chat(chat_id)

        except TimeoutError:
            await asyncio.sleep(20)
