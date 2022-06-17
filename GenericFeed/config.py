# Config file to generic feed
#
# Made by Luska1331
import os

# Pyrogram requirements

API_ID: int = os.environ.get("API_ID") or None
API_HASH: str = os.environ.get("API_HASH") or None
BOT_TOKEN: str = os.environ.get("BOT_TOKEN") or None

# GenericFeed requirements
MONGODB_URI: str = os.environ.get("MONGODB_URI") or None
OWNER_ID: int = 1874598662 # @Luska1331 xD
DEV_LIST: list = []
DEV_LIST.append(OWNER_ID)

FEED_FORMATTER_TEMPLATE: str = """
**{title}**

__{summary}__

Via [{feed_title}]({url})</a>
"""

HELP: dict = {}
