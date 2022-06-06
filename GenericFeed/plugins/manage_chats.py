from pyrogram import Client, filters
from pyrogram.types import (
        Message, CallbackQuery,
        InlineKeyboardButton, InlineKeyboardMarkup
)
from typing import Union
from GenericFeed.chat import Chat
from GenericFeed.utils import is_sudoer


@Client.on_message(filters.command(["addchat"]) & is_sudoer)  # addchat
async def add_chat(client: Client, message: Message):
    chat_manager = Chat()
    if chat_manager.check_chat(message.chat.id):
        await message.reply_text("Chat already added")
        return

    chat_manager.add_chat(message.chat.id, message.chat.title)
    await message.reply_text("Chat added")


@Client.on_message(filters.command(["removechat"]) & is_sudoer)  # removechat
async def remove_chat(client: Client, message: Message):
    chat_manager = Chat()
    if not chat_manager.check_chat(message.chat.id):
        await message.reply_text("Chat not found")
        return

    chat_manager.remove_chat(message.chat.id)
    await message.reply_text("Chat removed")


@Client.on_callback_query(filters.regex("listchats_back") & is_sudoer)  # listchats_back
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
                chat['chat_name'],
                callback_data="viewchat|" + str(chat['chat_id'])
            )
        )

    reply_markup = InlineKeyboardMarkup(
        [buttons[i:i+1] for i in range(0, len(buttons), 1)]
    )
    if is_callback:
        await union.message.edit_text(
            "Chats found:",
            reply_markup=reply_markup
        )
    else:
        await union.reply_text(
            "Chats found:",
            reply_markup=reply_markup
        )


@Client.on_callback_query(filters.regex("viewchat") & is_sudoer)  # viewchat
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
    back_button = InlineKeyboardButton(
        "Back",
        callback_data="listchats_back"
    )
    await callback_query.message.edit_text(
        chat_info_text,
        reply_markup=InlineKeyboardMarkup([[back_button]])
    )
