from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from typing import Union
from GenericFeed.chat import Chat
from GenericFeed.utils import is_sudoer
from GenericFeed.config import HELP

HELP["Manage chats"] = {
    'addchat': (
        "Add a chat to the list of managed chats.\n"
        "Usage: `/addchat (chat_id)?`\n"
    ),
    'removechat': (
        "Remove a chat from the list of managed chats.\n"
        "Send a message to the chat to remove it from the list of managed chats.\n"
        "Usage: `/removechat`\n"
    ),
    'listchats': (
        "List all managed chats.\n"
        "Send the list of managed chats to the chat.\n"
        "Usage: `/listchats`\n"
    )
}


@Client.on_message(filters.command(["addchat"]) & is_sudoer)  # addchat
async def add_chat(client: Client, message: Message):
    chat_manager = Chat()
    split_message = message.text.split(" ")
    if len(split_message) >= 2:
        chat_info = await client.get_chat(split_message[1])
        chat_id = chat_info.id
        chat_name = chat_info.title or chat_info.first_name
    else:
        chat_id = message.chat.id
        chat_name = message.chat.title or message.chat.first_name

    if chat_manager.check_chat(chat_id):
        await message.reply_text("Chat already added")
        return

    if chat_manager.add_chat(chat_id, chat_name):
        await message.reply_text(
            f"{chat_name} has been added to the list of managed chats."
        )


@Client.on_message(filters.command(["removechat"]) & is_sudoer)  # removechat
async def remove_chat(client: Client, message: Message):
    chat_manager = Chat()

    button_list = []
    for chat_item in chat_manager.get_chats():
        button_list.append(
            InlineKeyboardButton(
                chat_item["chat_name"],
                callback_data=f"removechat|{chat_item['chat_id']}",
            )
        )

    reply_markup = InlineKeyboardMarkup(
        [button_list[i : i + 2] for i in range(0, len(button_list), 2)]
    )

    await message.reply_text("Select chat to remove", reply_markup=reply_markup)


@Client.on_callback_query(filters.regex("^listchats_back") & is_sudoer)  # listchats_back
@Client.on_message(filters.command(["listchats"]) & is_sudoer)  # listchats
async def list_chats(client: Client, union: Union[Message, CallbackQuery]):
    chat_manager = Chat()
    chats = chat_manager.get_chats()
    is_callback = isinstance(union, CallbackQuery)
    if not chats and not is_callback:
        await union.reply_text("No chats found")
        return

    buttons = []

    for chat in chats:
        buttons.append(
            InlineKeyboardButton(
                chat["chat_name"], callback_data="viewchat|" + str(chat["chat_id"])
            )
        )

    reply_markup = InlineKeyboardMarkup(
        [buttons[i : i + 1] for i in range(0, len(buttons), 1)]
    )
    if is_callback:
        await union.message.edit_text("Chats found:", reply_markup=reply_markup)
    else:
        await union.reply_text("Chats found:", reply_markup=reply_markup)


@Client.on_callback_query(filters.regex("^removechat") & is_sudoer)  # remove_chat
async def remove_chat_callback(client: Client, callback: CallbackQuery):
    chat_manager = Chat()
    chat_id = callback.data.split("|")[1]
    deleted_chat_info = await client.get_chat(chat_id)
    deleted = chat_manager.remove_chat(int(deleted_chat_info.id))
    chat_name = deleted_chat_info.title or deleted_chat_info.first_name
    if deleted:
        await callback.message.edit_text(f"{chat_name} removed")
    else:
        await callback.message.edit_text(f"{chat_name} not found")


@Client.on_callback_query(filters.regex("^viewchat") & is_sudoer)  # viewchat
async def view_chat(client: Client, callback_query: CallbackQuery):
    chat_manager = Chat()
    data, chat_id = callback_query.data.split("|")
    chat = chat_manager.get_chat(int(chat_id))
    if not chat:
        await callback_query.answer("Chat not found")
        return

    chat_info = await client.get_chat(chat["chat_id"])
    chat_info_text = (
        f"Chat ID: {chat_info.id}\n"
        f"Chat title: {chat_info.title}\n"
        f"Chat type: {chat_info.type}\n"
        "Chat members count: " + str(chat_info.members_count) + "\n"
        "Chat description: " + chat_info.description + "\n"
        f"Chat invite link: {chat_info.invite_link or None}\n"
    )
    back_button = InlineKeyboardButton("Back", callback_data="listchats_back")
    await callback_query.message.edit_text(
        chat_info_text, reply_markup=InlineKeyboardMarkup([[back_button]])
    )
