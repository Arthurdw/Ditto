# Copyright Arthurdw 2021-present
# Full MIT License can be found in `LICENSE` at the project root.

from os import getenv

from colorama import Style
from dotenv import load_dotenv
from pincer import Client, __version__

from utils import LogLevel, log


class Ditto(Client):
    def __init__(self, token: str):
        log.set_level(LogLevel.INFO)
        log.info("Instantiating Ditto client on Pincer version", __version__)
        super().__init__(token)

    @Client.event
    async def on_ready(self):
        log.info("Successfully started on" + Style.BRIGHT, self.bot)


if __name__ == '__main__':
    load_dotenv()
    Ditto(getenv("BOT_TOKEN")).run()
