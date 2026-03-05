from dataclasses import dataclass, replace
from datetime import datetime, timezone
from uuid import UUID

from src.domain.value_objects import PromptContent, VersionNumber


@dataclass(frozen=True)
class PromptVersion:
    id: UUID
    prompt_id: UUID
    version_number: VersionNumber
    content: PromptContent
    created_at: datetime
    is_active: bool = False

    def _as_active(self) -> "PromptVersion":
        return replace(self, is_active=True)

    def _as_inactive(self) -> "PromptVersion":
        return replace(self, is_active=False)
