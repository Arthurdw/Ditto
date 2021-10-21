# Copyright Arthurdw 2021-present
# Full MIT License can be found in `LICENSE` at the project root.

from glob import glob
from os import getenv
from typing import Dict, Any
from uuid import UUID

from colorama import Style
from dotenv import load_dotenv
from pincer import Client, __version__

from utils import LogLevel, log, Webserver, DB, Webhook, WebhookType


class Ditto(Client):
    def __init__(self, token: str):
        log.set_level(LogLevel.INFO)
        log.info("Instantiating Ditto client on Pincer version", __version__)
        Webserver()
        Webserver.callbacks["webhook"] = self.webhook_handler
        self.load_cogs()
        self.db = DB()
        super().__init__(token)
        # self.db.create_webhook(Webhook(
        #     UUID("857188e6-329c-11ec-95fe-e73fb543f0f7"),
        #     WebhookType.DISCORD,
        #     "728278830770290759",
        #     "728284689261002832",
        #     ["728284888666603591", "776227954656280577"],
        #     ["232182858251239424", "640625683797639181"]
        # ))

    def load_cogs(self):
        """Load all cogs from the `cogs` directory."""
        for cog in glob("cogs/*.py"):
            self.load_cog(cog.replace("/", ".").replace("\\", ".")[:-3])

    async def webhook_handler(self, hook: UUID, data: Dict[str, Any]):
        webhook = self.db.get_webhook(hook)
        print(webhook)

    @Client.event
    async def on_ready(self):
        log.info("Successfully started on" + Style.BRIGHT, self.bot)


if __name__ == '__main__':
    load_dotenv()
    Ditto(getenv("BOT_TOKEN")).run()
