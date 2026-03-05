from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.domain.enums import PromptStatus
from src.domain.events import (
    DomainEvent,
    PromptCreated,
    PromptRecovered,
    PromptSoftDeleted,
    PromptVersionActivated,
    PromptVersionAdded,
)
from src.domain.exceptions import (
    PromptAlreadyDeletedException,
    PromptDeletedException,
    PromptNotDeletedException,
    VersionNotFoundException,
)
from src.domain.prompt_version import PromptVersion
from src.domain.value_objects import PromptContent, PromptName, VersionNumber


class Prompt:
    def __init__(
        self,
        id: UUID,
        name: PromptName,
        status: PromptStatus,
        active_version_id: UUID | None,
        created_at: datetime,
        updated_at: datetime,
        versions: list[PromptVersion] | None = None,
        events: list[DomainEvent] | None = None,
    ):
        self.id = id
        self.name = name
        self.status = status
        self.active_version_id = active_version_id
        self.created_at = created_at
        self.updated_at = updated_at
        self._versions: list[PromptVersion] = versions or []
        self._events: list[DomainEvent] = events or []

    @classmethod
    def create(cls, name: PromptName) -> "Prompt":
        now = datetime.now(timezone.utc)
        prompt_id = uuid4()
        prompt = cls(
            id=prompt_id,
            name=name,
            status=PromptStatus.INACTIVE,
            active_version_id=None,
            created_at=now,
            updated_at=now,
        )
        prompt._events.append(PromptCreated(prompt_id=prompt_id, name=name.value))
        return prompt

    def add_version(self, content: PromptContent) -> PromptVersion:
        if self.status == PromptStatus.DELETED:
            raise PromptDeletedException(self.id)

        if self._versions:
            next_number = max(v.version_number for v in self._versions).next()
        else:
            next_number = VersionNumber(1)

        version = PromptVersion(
            id=uuid4(),
            prompt_id=self.id,
            version_number=next_number,
            content=content,
            created_at=datetime.now(timezone.utc),
            is_active=False,
        )
        self._versions.append(version)
        self.updated_at = datetime.now(timezone.utc)
        self._events.append(
            PromptVersionAdded(
                prompt_id=self.id,
                version_id=version.id,
                version_number=version.version_number.value,
            )
        )
        return version

    def activate_version(self, version_id: UUID) -> None:
        if self.status == PromptStatus.DELETED:
            raise PromptDeletedException(self.id)

        target = next((v for v in self._versions if v.id == version_id), None)
        if target is None:
            raise VersionNotFoundException(version_id, self.id)

        previously_active_id = self.active_version_id

        self._versions = [
            v._as_inactive() if v.is_active else v for v in self._versions
        ]
        self._versions = [
            v._as_active() if v.id == version_id else v for v in self._versions
        ]

        self.active_version_id = version_id
        self.status = PromptStatus.ACTIVE
        self.updated_at = datetime.now(timezone.utc)
        self._events.append(
            PromptVersionActivated(
                prompt_id=self.id,
                version_id=version_id,
                previously_active_id=previously_active_id,
            )
        )

    def soft_delete(self) -> None:
        if self.status == PromptStatus.DELETED:
            raise PromptAlreadyDeletedException(self.id)

        self.status = PromptStatus.DELETED
        self.active_version_id = None
        self._versions = [v._as_inactive() for v in self._versions]
        self.updated_at = datetime.now(timezone.utc)
        self._events.append(PromptSoftDeleted(prompt_id=self.id))

    def recover(self) -> None:
        if self.status != PromptStatus.DELETED:
            raise PromptNotDeletedException(self.id)

        self.status = PromptStatus.INACTIVE
        self.updated_at = datetime.now(timezone.utc)
        self._events.append(PromptRecovered(prompt_id=self.id))

    def collect_events(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events
