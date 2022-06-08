from pyrogram import Client, filters
from pyrogram.types import (
    Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
)
from GenericFeed.config import HELP
from typing import Union


@Client.on_callback_query(filters.regex(r"help_back"))
@Client.on_message(filters.command("help"))
async def help(client: Client, union: Union[Message, CallbackQuery]):
    is_callback = isinstance(union, CallbackQuery)
    help_message = ""
    buttons = []
    for group in HELP.keys():
        buttons.append(
            InlineKeyboardButton(
                group,
                callback_data=f"help_{group}"
            )
        )
    help_message += "Select a group to see its commands:\n"
    markup = InlineKeyboardMarkup(
        [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    )
    if is_callback:
        await union.message.edit_text(
            help_message,
            reply_markup=markup
        )
        return
    await union.reply_text(
        help_message,
        reply_markup=markup
    )


@Client.on_callback_query(filters.regex("help_.*"))
async def help_group(client: Client, query: CallbackQuery):
    group = query.data.split("_")[1]
    help_message = "Commands for group: `{}`\n".format(group)
    buttons = []
    for command in HELP[group].keys():
        buttons.append(
            InlineKeyboardButton(
                f"/{command}",
                callback_data=f"command_{group}_{command}"
            )
        )

    buttons.append(
        InlineKeyboardButton("Back",callback_data="help_back")
    )

    await query.message.edit_text(
        help_message,
        reply_markup=InlineKeyboardMarkup(
            [buttons[i:i+2] for i in range(0, len(buttons), 2)],

        )
    )


@Client.on_callback_query(filters.regex(r"command_.*"))
async def help_command(client: Client, query: CallbackQuery):
    group = query.data.split("_")[1]
    command = query.data.split("_")[2]
    help_message = "Command: `{}`\n".format(command)
    help_message += "Description: {}\n".format(HELP[group][command])
    back_group = InlineKeyboardButton(
        "Back",
        callback_data=f"help_{group}"
    )

    await query.message.edit_text(
        help_message,
        reply_markup=InlineKeyboardMarkup([[back_group]])
    )
