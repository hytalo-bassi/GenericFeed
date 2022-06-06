# Commands to manage feeds
import requests
from pyrogram import Client, filters
from pyrogram.types import (
    Message, CallbackQuery,
    InlineKeyboardButton, InlineKeyboardMarkup
)
from GenericFeed.feed import Feed
from typing import Union
from GenericFeed.utils import is_sudoer

@Client.on_message(filters.command("addfeed") & is_sudoer)  # addfeed <url> <name>
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


@Client.on_message(filters.command("removefeed") & is_sudoer)  # removefeed
async def remove_feed(client: Client, message: Message):
    feed = Feed()
    buttons = []

    for feed in feed.get_feeds():
        buttons.append(
            InlineKeyboardButton(
                feed['name'],
                callback_data="removefeed|" + str(feed["_id"])
            )
        )

    markup = InlineKeyboardMarkup(
        [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    )

    await client.send_message(
        message.chat.id,
        "Select a feed to remove",
        reply_markup=markup
    )


@Client.on_callback_query(filters.regex("removefeed") & is_sudoer)  # removefeed <id>
async def remove_feed_callback(client: Client, callback_query: CallbackQuery):
    feed = Feed()
    feed_id = callback_query.data.split("|")[1]

    success = feed.remove_feed(feed_id)
    if success:
        await callback_query.answer("Feed removed successfully!")
    else:
        await callback_query.answer("Feed does not exist!")
        return

    await callback_query.message.delete()


@Client.on_callback_query(filters.regex("listfeeds_back") & is_sudoer)  # addfeed <id>
@Client.on_message(filters.command("listfeeds") & is_sudoer)  # listfeeds
async def list_feeds(client: Client, union: Union[Message, CallbackQuery]):

    feed = Feed()

    is_callback = isinstance(union, CallbackQuery)
    buttons = []

    for feed in feed.get_feeds():
        buttons.append(
            InlineKeyboardButton(
                feed['name'],
                callback_data="listfeeds|" + str(feed["_id"])
            )
        )

    markup = InlineKeyboardMarkup(
        [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    )
    if not is_callback:
        await client.send_message(
            union.chat.id,
            "Select a feed to view",
            reply_markup=markup
        )
        return
    else:
        await union.message.edit_text(
            "Select a feed to view",
            reply_markup=markup
        )


@Client.on_callback_query(filters.regex("listfeeds") & is_sudoer)  # listfeeds <id>
async def list_feeds_callback(client: Client, callback_query: CallbackQuery):
    feed = Feed()
    feed_id = callback_query.data.split("|")[1]

    feed_data = feed.get_feed(feed_id)
    if feed_data is None:
        await callback_query.answer("Feed does not exist!")
        return

    buttons = [
        InlineKeyboardButton(
            "Back",
            callback_data="listfeeds_back"
        )
    ]

    await callback_query.message.edit_text(
        "Feed name: " + feed_data["name"] + "\nURL: " + feed_data["url"],
        reply_markup=InlineKeyboardMarkup(
            [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
        )
    )


@Client.on_message(filters.command("clearfeeds") & is_sudoer)  # clearfeeds
async def clear_feeds(client: Client, message: Message):
    feed = Feed()
    feeds = feed.get_feeds()
    msg = await message.reply_text("Clearing feeds...")

    for feed_item in feeds:
        feed.clear_last_update(feed_item["url"])

    await msg.edit_text(msg.text + "\nAll feeds cleared!")
