# Commands to manage feeds
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from GenericFeed.feed import Feed


@Client.on_message(filters.command("addfeed"))  # addfeed <url> <name>
async def add_feed(client: Client, message: Message):
    feed = Feed()
    split_message = message.text.split(" ")

    if len(split_message) < 3:
        await message.reply_text("Usage: /addfeed (url) (name)")
        return

    feed_url = split_message[1]
    feed_name = " ".join(split_message[2:])

    # Check if feed url works
    try:
        requests.get(feed_url)
    except requests.exceptions.RequestException:
        await message.reply_text("Invalid feed url")
        return

    msg = await client.send_message(
        message.chat.id,
        "Adding feed: " + feed_name + "\nWith url: " + feed_url
    )

    success = feed.add_feed(feed_name, feed_url)
    if success:
        await msg.edit_text(
            "Feed added successfully!"
        )
    else:
        await msg.edit_text(
            "Feed already exists!"
        )
