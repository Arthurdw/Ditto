# Copyright Arthurdw 2021-present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, List

from pincer.objects import Embed, Message
from utils import Webserver, log, WebhookType

if TYPE_CHECKING:
    from pincer.objects import Channel
    from pincer.utils import Snowflake
    from uuid import UUID
    from run import Ditto
    from typing import Dict, Any
    from utils import Webhook


class Webhooks:
    __cache: Dict[str, Dict[Snowflake, Channel]] = defaultdict(dict)

    def __init__(self, client: Ditto):
        self.client = client
        log.debug("Starting webserver...")
        Webserver()
        Webserver.callbacks["webhook"] = self.webhook_handler
        log.debug("Successfully started webserver!")

        self.__handlers = {
            WebhookType.GITHUB: self.process_github_hook
        }

        # self.db.create_webhook(Webhook(
        #     UUID("857188e6-329c-11ec-95fe-e73fb543f0f7"),
        #     WebhookType.GITHUB,
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

        if handler := self.__handlers.get(webhook.hook_type):
            await handler(webhook, channel, data)

    @staticmethod
    def convert_github_commit(data: Dict[str, Any]) -> List[Embed]:
        commits = list(filter(lambda commit: commit["author"].get("username"), data["commits"]))

        def form_commit_small(commit: Dict[str, Any]) -> str:
            message = commit['message']

            if len(message) > 38:
                message = message[:36] + "..."

            return f"[`{commit['id'][:7]}`]({commit['url']}) {message} - {commit['author']['name']}"

        changes = "\n".join(map(form_commit_small, commits))

        append = ""
        if len(changes) > 2000:
            append = "..."

        def form_changes_embed(commit: Dict[str, Any]) -> Embed:
            embed = Embed(
                color=0x42579e,
            ).set_author(
                name=commit["message"],
                url=commit["url"]
            ).set_footer(
                text=f"Pushed by {commit['author']['username']}"
            )

            for title, diff, file_changes in [
                ("Added", "+ ", commit["added"]),
                ("Modified", "! ", commit["modified"]),
                ("Removed", "- ", commit["removed"])
            ]:
                if file_changes:
                    embed.add_field(
                        name=title,
                        value="```diff\n" +
                              "\n".join([diff + change for change in file_changes]) +
                              "\n```"
                    )

            return embed

        embeds = [
            Embed(
                color=0x738adb,
                description=changes[:1997] + append
            ).set_author(
                icon_url=data["sender"]["avatar_url"],
                name=f"{len(data['commits'])} new commits",
                url=data["compare"]
            ).set_footer(
                text=data["repository"]["name"],
                icon_url=data["repository"]["owner"]["avatar_url"]
            ),
            *list(map(form_changes_embed, commits))
        ]

        return embeds

    async def process_github_hook(self, webhook: Webhook, channel: Channel, data: Dict[str, Any]):
        embeds = self.convert_github_commit(data)

        await channel.send(Message(
            "".join(
                [f"<@&{role}>" for role in webhook.role_mentions] +
                [f"<@!{user}>" for user in webhook.user_mentions]
            ),
            embeds=[embeds.pop(0)]
        ))

        for i in range(len(embeds) // 10):
            await channel.send(Message(embeds=embeds[i * 10:i * 10 + 10]))


setup = Webhooks
