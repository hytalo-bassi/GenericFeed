import asyncio
import feedparser
from pyrogram import Client
from GenericFeed.config import (
        BOT_TOKEN, API_ID,
        API_HASH, CHAT_LIST,
        FEED_FORMATTER_TEMPLATE
)
from GenericFeed.feed import Feed


async def StartFeedLoop(bot: Client):
    while True:
        feed = Feed()
        feed_items = feed.get_feeds()  # Get feeds from the API
        for item in feed_items:
            print('-+-' * 20)
            feed_url = item['url']
            print(f'[+] Feed URL: {feed_url}')
            have_update = feed.check_update(feed_url)  # Check if there is an update
            print(f'[+] Have update: {have_update}')
            if have_update:
                feed.update_feed(feed_url)  # Update the feeds
                feed_item = feedparser.parse(feed_url)  # Parse the feed
                for chat in CHAT_LIST:
                    print(f'[+] Sending to chat: {chat}')
                    await bot.send_message(
                        chat_id=chat,
                        text=FEED_FORMATTER_TEMPLATE.format(
                            feed_title=feed_item['feed']['title'],
                            title=feed_item.entries[0].title,
                            url=feed_item.entries[0].link,
                            summary=feed_item.entries[0].summary,
                        )
                    )
        await asyncio.sleep(60)


class GenericFeed(Client):
    def __init__(self):
        super().__init__(
            "GenericFeed",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=4,
            plugins=dict(
                root="GenericFeed/plugins"
            ),
        )

    async def start(self):
        await super().start()
        await StartFeedLoop(self)
