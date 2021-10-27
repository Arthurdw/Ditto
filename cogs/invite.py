# Copyright Arthurdw 2021-present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from typing import TYPE_CHECKING

from pincer import command
from pincer.objects import Message, InteractionFlags

if TYPE_CHECKING:
    from run import Ditto


class Invite:
    def __init__(self, client: Ditto):
        self.client = client

    @command()
    async def invite(self):
        return Message(
            f"https://discord.com/api/oauth2/authorize?client_id={self.client.bot.id}"
            f"&scope=bot%20applications.commands",
            flags=InteractionFlags.EPHEMERAL
        )


setup = Invite
