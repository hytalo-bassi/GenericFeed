from pyrogram import Client, filters
from pyrogram.types import Message

from GenericFeed.loop import LoopController


@Client.on_message(filters.command("loop"))
async def loop_command(client: Client, message: Message):
    loop = LoopController()
    args = message.text.split(" ")
    if len(args) == 1:
        status = loop.get_loop_status()
        await message.reply_text(
            f"Loop is {'enabled' if status else 'disabled'}"
        )

    elif len(args) == 2:
        if args[1] == "enable":
            loop.set_loop_status(True)
            await message.reply_text("Loop enabled")
        elif args[1] == "disable":
            loop.set_loop_status(False)
            await message.reply_text("Loop disabled")
        else:
            await message.reply_text(
                "Invalid argument\n"
                "Usage: /loop [enable|disable]"
            )
