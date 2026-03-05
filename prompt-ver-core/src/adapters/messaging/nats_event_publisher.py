import json
from datetime import datetime
from uuid import UUID

import nats.aio.client as nats_client

from src.domain.events import (
    DomainEvent,
    PromptCreated,
    PromptRecovered,
    PromptSoftDeleted,
    PromptVersionActivated,
    PromptVersionAdded,
)
from src.ports.event_publisher import EventPublisher

_EVENT_SUBJECTS: dict[type[DomainEvent], str] = {
    PromptCreated: "prompts.v1.events.prompt_created",
    PromptVersionAdded: "prompts.v1.events.version_added",
    PromptVersionActivated: "prompts.v1.events.version_activated",
    PromptSoftDeleted: "prompts.v1.events.prompt_deleted",
    PromptRecovered: "prompts.v1.events.prompt_recovered",
}


def _coerce(obj):
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


class NatsEventPublisher(EventPublisher):
    def __init__(self, nc: nats_client.Client) -> None:
        self._nc = nc

    async def publish(self, events: list[DomainEvent]) -> None:
        for event in events:
            subject = _EVENT_SUBJECTS.get(type(event))
            if subject is None:
                continue
            payload = {
                k: _coerce(v) for k, v in vars(event).items()
            }
            payload["event_type"] = type(event).__name__
            data = json.dumps(payload).encode()
            await self._nc.publish(subject, data)
