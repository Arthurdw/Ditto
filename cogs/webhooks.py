# Copyright Arthurdw 2021-present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from typing import TYPE_CHECKING, List
from uuid import uuid4

from pincer import command, Choices, Descripted
from pincer.objects import Embed, Message, InteractionFlags
from pincer.objects.guild import TextChannel
from utils import Webhook
from utils import Webserver, log, WebhookType

if TYPE_CHECKING:
    from pincer.objects import Channel
    from pincer.utils import Snowflake
    from uuid import UUID
    from run import Ditto
    from typing import Dict, Any


class Webhooks:
    __cache: Dict[Snowflake, Channel] = {}

    def __init__(self, client: Ditto):
        self.client = client
        log.debug("Starting webserver...")
        Webserver()
        Webserver.callbacks["webhook"] = self.webhook_handler
        log.debug("Successfully started webserver!")

        self.__handlers = {
            WebhookType.GITHUB_PUSH: self.process_github_push_hook
        }

    async def webhook_handler(self, hook: UUID, data: Dict[str, Any]):
        webhook = self.client.db.get_webhook(hook)
        channel = Webhooks.__cache.get(webhook.channel)

        if not channel:
            channel = await self.client.get_channel(int(webhook.channel))
            Webhooks.__cache[channel.id] = channel

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

    async def process_github_push_hook(self, webhook: Webhook, channel: Channel, data: Dict[str, Any]):
        try:
            embeds = self.convert_github_commit(data)
        except KeyError:
            return

        await channel.send(Message(
            "".join(
                [f"<@&{role}>" for role in webhook.role_mentions] +
                [f"<@!{user}>" for user in webhook.user_mentions]
            ),
            embeds=[embeds.pop(0)]
        ))

        for i in range(len(embeds) // 10):
            await channel.send(Message(embeds=embeds[i * 10:i * 10 + 10]))

    @command(
        description="Create a new webhook!",
        guild=728278830770290759,

        cooldown=10
    )
    async def add(
            self,
            notification: Descripted[
                Choices[
                    Descripted['1', "github push notifications"]
                ],
                "The type of webhook you want to add!"
            ],
            channel: Descripted[
                Channel,
                "The channel to whom the message should be sent when the webhook has been invoked."
            ]
    ):
        if not isinstance(channel, TextChannel):
            return Message(
                embeds=[
                    Embed(
                        description="Can only send the webhook updates to a text channel!",
                        color=0xff0000
                    )
                ],
                flags=InteractionFlags.EPHEMERAL
            )

        webhook = Webhook(
            id=uuid4(),
            hook_type=WebhookType(int(notification)),
            guild=str(channel.guild_id),
            channel=str(channel.id),
            role_mentions=[],
            user_mentions=[]
        )

        self.client.db.create_webhook(webhook)
        return Message(
            embeds=[
                Embed(
                    description=f"""Successfully created webhook!
                    Please add the following url to your github push event:
                    [`{Webserver.url}/webhook/{webhook.id}`]({Webserver.url}/webhook/{webhook.id})
                    """,
                    color=0x00ff00
                )
            ],
            flags=InteractionFlags.EPHEMERAL
        )


setup = Webhooks
