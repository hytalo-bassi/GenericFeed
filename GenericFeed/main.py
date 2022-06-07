import asyncio
import feedparser

from pyrogram import Client
from pyrogram.errors import (
    ChatIdInvalid,
    PeerIdInvalid,
    ChannelPrivate,
    UserIsBlocked,
    UserIsBot,
    MessageTooLong
)

from GenericFeed.config import (
    BOT_TOKEN, API_ID, API_HASH,
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
        feed_items = feed.get_feeds()  # Get feeds from the DB
        for item in feed_items:
            status = loop.get_loop_status()
            if status is False:
                await asyncio.sleep(60)
                continue

            feed_url = item["url"]
            print(f" [■] Feed URL: {feed_url}")
            have_update = feed.check_update(feed_url)  # Check if there is an update
            print(f" [+] Have update: {have_update}")
            if have_update:
                try:
                    feed.update_feed(feed_url)  # Update the feeds
                except IndexError:
                    print(" [!] Error: IndexError")
                    feed.remove_feed(item["_id"])  # Remove the feed from the DB
                    continue
                feed_item = feedparser.parse(feed_url)  # Parse the feed
                for chat in Chat().get_chats():
                    print(f' [+] Sending to: {chat["chat_name"]} | {chat["chat_id"]}')
                    try:
                        try:
                            text_content = feed_item.entries[0].summary
                        except AttributeError:
                            try:
                                text_content = feed_item.entries[0].description
                            except AttributeError:
                                text_content = "No description"
                        await bot.send_message(
                            chat_id=chat["chat_id"],
                            text=FEED_FORMATTER_TEMPLATE.format(
                                feed_title=feed_item["feed"]["title"],
                                title=feed_item.entries[0].title,
                                url=feed_item.entries[0].link,
                                summary=text_content  # Personal choice xD
                            ),
                        )
                    except (
                        ChatIdInvalid,
                        PeerIdInvalid,
                        ChannelPrivate,
                        UserIsBlocked,
                        UserIsBot,
                    ) as e:
                        print(
                            f' [!] Error sending message to {chat["chat_name"]} | {chat["chat_id"]}'
                        )
                        print(f" [!] Error: {e}")
                        print(" [!] Removing chat from DB")
                        Chat().remove_chat(chat["chat_id"])
                    except MessageTooLong:
                        await bot.send_message(
                            chat_id=chat["chat_id"],
                            text=FEED_FORMATTER_TEMPLATE.format(
                                feed_title=feed_item["feed"]["title"],
                                title=feed_item.entries[0].title,
                                url=feed_item.entries[0].link,
                                summary=text_content[:200],  # Personal choice xD
                            ),
                            parse_mode="HTML",
                        )

                    except Exception as e:
                        print(f" [!] Error sending message to {chat['chat_name']} | {chat['chat_id']}")
                        print(f" [!] Feed URL: {feed_url}")
                        print(f" [!] Error: {e}")
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
