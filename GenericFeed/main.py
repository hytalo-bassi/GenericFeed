import asyncio
import aiohttp
import feedparser
from pyrogram import Client
from pyrogram.errors import (
    ChatIdInvalid,
    PeerIdInvalid,
    ChannelPrivate,
    UserIsBlocked,
    UserIsBot,
    MessageTooLong,
)

from GenericFeed.config import (
    BOT_TOKEN,
    API_ID,
    API_HASH,
    FEED_FORMATTER_TEMPLATE
)
from GenericFeed.feed import Feed
from GenericFeed.chat import Chat
from GenericFeed.loop import LoopController


async def StartFeedLoop(bot: Client):
    feed = Feed()
    loop = LoopController()
    print("═" * 70)
    while True:
        feed_items = feed.get_feeds()
        for item in feed_items:
            status = loop.get_loop_status()
            if status is False:
                await asyncio.sleep(10)
                continue

            feed_url = item["url"]
            print(f" [■] Feed URL: {feed_url}")
            have_update = feed.check_update(feed_url)
            print(f" [+] Have update: {have_update}")
            if have_update:
                try:
                    feed.update_feed(feed_url)
                except IndexError:
                    print(" [!] Error: IndexError")
                    feed.remove_feed(item["_id"])
                    continue

                async with aiohttp.ClientSession() as session:
                    async with session.get(feed_url, timeout=10) as response:
                        html = await response.text()

                feed_item = feedparser.parse(html)
                for chat in Chat().get_chats():
                    print(
                        f' [✓] Sending to: {chat["chat_name"]} | {chat["chat_id"]}'
                    )
                    try:
                        await bot.send_feed(chat, feed_item)
                    except MessageTooLong:
                        await bot.send_feed(chat, feed_item, limit=200)
                    except KeyError:
                        print(" [!] Error: KeyError")
        print("═" * 70)
        await asyncio.sleep(60)


class GenericFeed(Client):
    def __init__(self):
        super().__init__(
            "GenericFeed",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=4,
            plugins=dict(root="GenericFeed/plugins"),
        )

    async def start(self):
        await super().start()
        await StartFeedLoop(self)

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
            text_content = text_content[:limit] + "..."

        try:
            image_content = last_entry["media_content"][0]["url"]
        except Exception:
            try:
                image_content = last_entry['image']
            except Exception:
                print(" [!] Error: No image found")
            image_content = None
        formatted_text = FEED_FORMATTER_TEMPLATE.format(
            feed_title=feed_data["feed"]["title"],
            title=last_entry.title,
            url=last_entry.link,
            summary=(
                text_content if len(text_content) >= 0 else "No description."
            ),
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
        ) as e:
            print(f" [!] Error sending message to {chat_id}")
            print(f" [!] Error: {e}")
            print(" [!] Removing chat from DB")
            Chat().remove_chat(chat_id)

        except TimeoutError:
            await asyncio.sleep(20)
