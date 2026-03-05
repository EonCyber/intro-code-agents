from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID


@dataclass(frozen=True)
class DomainEvent:
    prompt_id: UUID
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class PromptCreated(DomainEvent):
    name: str = ""


@dataclass(frozen=True)
class PromptVersionAdded(DomainEvent):
    version_id: UUID = None
    version_number: int = 0


@dataclass(frozen=True)
class PromptVersionActivated(DomainEvent):
    version_id: UUID = None
    previously_active_id: UUID | None = None


@dataclass(frozen=True)
class PromptSoftDeleted(DomainEvent):
    pass


@dataclass(frozen=True)
class PromptRecovered(DomainEvent):
    pass
