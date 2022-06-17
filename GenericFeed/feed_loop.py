import asyncio
import logging

import aiohttp
import feedparser
from pyrogram import Client
from pyrogram.errors import MediaCaptionTooLong, MessageTooLong

from GenericFeed.chat import Chat
from GenericFeed.feed import Feed
from GenericFeed.loop import LoopController


async def start_feed_loop(bot: Client):
    feed = Feed()
    loop = LoopController()
    while True:
        feed_items = feed.get_feeds()
        for item in feed_items:
            status = loop.get_loop_status()
            if status is False:
                await asyncio.sleep(10)
                continue

            feed_url = item["url"]
            have_update = feed.check_update(feed_url)
            if have_update:
                try:
                    feed.update_feed(feed_url)
                except IndexError:
                    feed.remove_feed(item["_id"])
                    continue

                async with aiohttp.ClientSession() as session:
                    async with session.get(feed_url, timeout=10) as response:
                        html = await response.text()

                feed_item = feedparser.parse(html)
                for chat in Chat().get_chats():
                    try:
                        await bot.send_feed(chat, feed_item)
                    except (MessageTooLong, MediaCaptionTooLong):
                        await bot.send_feed(chat, feed_item, limit=200)
                    except KeyError as err:
                        logging.error(f"KeyError: {err}")
        await asyncio.sleep(60)
