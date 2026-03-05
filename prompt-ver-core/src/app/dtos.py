from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


# Commands (input)

@dataclass(frozen=True)
class CreatePromptCommand:
    name: str


@dataclass(frozen=True)
class AddVersionCommand:
    prompt_id: UUID
    content: str


@dataclass(frozen=True)
class UpdateContentCommand:
    prompt_id: UUID
    content: str


@dataclass(frozen=True)
class ActivateVersionCommand:
    prompt_id: UUID
    version_id: UUID


@dataclass(frozen=True)
class SoftDeletePromptCommand:
    prompt_id: UUID


@dataclass(frozen=True)
class RecoverPromptCommand:
    prompt_id: UUID


# Queries (input)

@dataclass(frozen=True)
class GetPromptByIdQuery:
    prompt_id: UUID


@dataclass(frozen=True)
class ListVersionsQuery:
    prompt_id: UUID


# Queries (continued)

@dataclass(frozen=True)
class CompareVersionsQuery:
    prompt_id: UUID
    version_id_before: UUID
    version_id_after: UUID


# Responses (output)

@dataclass(frozen=True)
class PromptResponse:
    id: UUID
    name: str
    status: str
    active_version_id: UUID | None
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class PromptVersionResponse:
    id: UUID
    prompt_id: UUID
    version_number: int
    content: str
    created_at: datetime
    is_active: bool


@dataclass(frozen=True)
class DiffLineResponse:
    kind: str
    content: str
    line_number_before: int | None
    line_number_after: int | None


@dataclass(frozen=True)
class VersionDiffResponse:
    prompt_id: UUID
    version_id_before: UUID
    version_id_after: UUID
    version_number_before: int
    version_number_after: int
    lines: tuple[DiffLineResponse, ...]
    has_changes: bool


@dataclass(frozen=True)
class PromptDetailResponse:
    id: UUID
    name: str
    status: str
    active_version_id: UUID | None
    created_at: datetime
    updated_at: datetime
    versions: list[PromptVersionResponse]
