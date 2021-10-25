# Copyright Arthurdw 2021-present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from utils import Webserver, log

if TYPE_CHECKING:
    from pincer.objects import Channel
    from pincer.utils import Snowflake
    from uuid import UUID
    from run import Ditto
    from typing import Dict, Any


class Webhooks:
    __cache: Dict[str, Dict[Snowflake, Channel]] = defaultdict(dict)

    def __init__(self, client: Ditto):
        self.client = client
        log.debug("Starting webserver...")
        Webserver()
        Webserver.callbacks["webhook"] = self.webhook_handler
        log.debug("Successfully started webserver!")

        # self.db.create_webhook(Webhook(
        #     UUID("857188e6-329c-11ec-95fe-e73fb543f0f7"),
        #     WebhookType.DISCORD,
        #     "728278830770290759",
        #     "728284689261002832",
        #     ["728284888666603591", "776227954656280577"],
        #     ["232182858251239424", "640625683797639181"]
        # ))

    async def webhook_handler(self, hook: UUID, data: Dict[str, Any]):
        webhook = self.client.db.get_webhook(hook)
        channel = Webhooks.__cache[webhook.guild].get(webhook.channel)

        if not channel:
            channel = await self.client.get_channel(int(webhook.channel))
            Webhooks.__cache[webhook.guild][channel.id] = channel

        # TODO: Proper handling
        await channel.send(
            f"Received webhook `{hook}`\n" +
            "".join(
                [f"<@&{role}>" for role in webhook.role_mentions] +
                [f"<@!{user}>" for user in webhook.user_mentions]
            )
        )


setup = Webhooks
