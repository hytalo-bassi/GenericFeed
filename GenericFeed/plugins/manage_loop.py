from pyrogram import Client, filters
from pyrogram.types import Message

from GenericFeed.config import HELP
from GenericFeed.loop import LoopController

HELP["Manage loop"] = {
    "loop": ("Manage the loop of the bot.\n" "Usage: `/loop (start|stop|status)`\n"),
}


@Client.on_message(filters.command("loop"))
async def loop_command(client: Client, message: Message):
    loop = LoopController()
    args = message.text.lower().split(" ")

    if len(args) == 2:
        if args[1] == "start":
            loop.set_loop_status(True)
            await message.reply_text("Loop enabled")
        elif args[1] == "stop":
            loop.set_loop_status(False)
            await message.reply_text("Loop disabled")
        elif args[1] == "status":
            await message.reply_text(
                "Loop is " + ("enabled" if loop.get_loop_status() else "disabled")
            )
        else:
            await message.reply_text(HELP["Manage loop"]["loop"])
    else:
        await message.reply_text(HELP["Manage loop"]["loop"])
