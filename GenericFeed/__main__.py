import datetime
import logging
from os import path

from GenericFeed.client import GenericFeed
from GenericFeed.config import API_HASH, API_ID, BOT_TOKEN
from GenericFeed.feed_loop import start_feed_loop

app = GenericFeed(API_ID, API_HASH, BOT_TOKEN)
LOGDIR = "logs"


async def main():
    await app.start()
    await start_feed_loop(app)


def log_file():
    now = datetime.datetime.now()
    filename = now.strftime("%Y-%m-%dT%H:%M")

    return path.join(LOGDIR, filename + ".log")


if not path.exists(LOGDIR):
    path.mkdir(LOGDIR)


logging.basicConfig(
    filename=log_file(), level=logging.DEBUG, format="%(asctime)s %(message)s"
)

if __name__ == "__main__":
    app.run(main())
