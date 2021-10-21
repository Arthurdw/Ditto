# Copyright Arthurdw 2021-present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass
from enum import IntEnum
from typing import List, Tuple, Any
from uuid import UUID


class WebhookType(IntEnum):
    DISCORD = 1


@dataclass
class Webhook:
    id: UUID
    hook_type: WebhookType
    guild: str
    channel: str
    role_mentions: List[str]
    user_mentions: List[str]

    def serialize(self) -> Tuple[UUID, Any, str, str, List[str], List[str]]:
        return (
            self.id,
            self.hook_type.value,
            self.guild,
            self.channel,
            self.role_mentions,
            self.user_mentions
        )
