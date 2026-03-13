from datetime import datetime
from typing import Generic, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel

T = TypeVar("T")


class EventWrapper(BaseModel, Generic[T]):
    """Generic wrapper for all NATS event responses."""

    ok: bool
    data: T


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------

class PromptResponse(BaseModel):
    id: UUID
    name: str
    status: str
    active_version_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    content: Optional[str] = None


class PromptVersionResponse(BaseModel):
    id: UUID
    prompt_id: UUID
    version_number: int
    content: str
    created_at: datetime
    is_active: bool


class DiffLineResponse(BaseModel):
    kind: str
    content: str
    line_number_before: Optional[int] = None
    line_number_after: Optional[int] = None


class VersionDiffResponse(BaseModel):
    prompt_id: UUID
    version_id_before: UUID
    version_id_after: UUID
    version_number_before: int
    version_number_after: int
    lines: list[DiffLineResponse]
    has_changes: bool


class PromptDetailResponse(BaseModel):
    id: UUID
    name: str
    status: str
    active_version_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    versions: list[PromptVersionResponse]


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class CreatePromptRequest(BaseModel):
    name: str
    content: str


class AddVersionRequest(BaseModel):
    prompt_id: str
    content: str


class UpdateContentRequest(BaseModel):
    prompt_id: str
    content: str


class ActivateVersionRequest(BaseModel):
    prompt_id: str
    version_id: str


class GetPromptByIdRequest(BaseModel):
    prompt_id: str


class ListVersionsRequest(BaseModel):
    prompt_id: str


class ListActivePromptsRequest(BaseModel):
    pass


class CompareVersionsRequest(BaseModel):
    prompt_id: str
    version_id_before: str
    version_id_after: str


class SoftDeletePromptRequest(BaseModel):
    prompt_id: str


class ListDeletedPromptsRequest(BaseModel):
    pass


class RecoverPromptRequest(BaseModel):
    prompt_id: str


# Body-only models for endpoints where prompt_id comes from the URL path

class AddVersionBody(BaseModel):
    content: str


class UpdateContentBody(BaseModel):
    content: str


class ActivateVersionBody(BaseModel):
    version_id: str


class CompareVersionsBody(BaseModel):
    version_id_before: str
    version_id_after: str
