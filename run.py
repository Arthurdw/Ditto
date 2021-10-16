# Copyright Arthurdw 2021-present
# Full MIT License can be found in `LICENSE` at the project root.

from glob import glob
from os import getenv
from typing import Dict, Any

from colorama import Style
from dotenv import load_dotenv
from pincer import Client, __version__

from utils import LogLevel, log, Webserver


class Ditto(Client):
    def __init__(self, token: str):
        log.set_level(LogLevel.INFO)
        log.info("Instantiating Ditto client on Pincer version", __version__)
        Webserver()
        Webserver.callbacks["webhook"] = self.webhook_handler
        self.load_cogs()
        super().__init__(token)

    def load_cogs(self):
        """Load all cogs from the `cogs` directory."""
        for cog in glob("cogs/*.py"):
            self.load_cog(cog.replace("/", ".").replace("\\", ".")[:-3])

    async def webhook_handler(self, hook: str, data: Dict[str, Any]):
        print(hook, data)

    @Client.event
    async def on_ready(self):
        log.info("Successfully started on" + Style.BRIGHT, self.bot)


if __name__ == '__main__':
    load_dotenv()
    Ditto(getenv("BOT_TOKEN")).run()
