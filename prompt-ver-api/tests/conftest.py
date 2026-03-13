import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock

from controllers.routes import router
from models.prompt_models import (
    DiffLineResponse,
    PromptDetailResponse,
    PromptResponse,
    PromptVersionResponse,
    VersionDiffResponse,
)
from utils.error_handlers import app_exception_handler, generic_exception_handler
from utils.exceptions import BaseAppException

from datetime import datetime
from uuid import UUID

PROMPT_ID = UUID("00000000-0000-0000-0000-000000000001")
VERSION_ID = UUID("00000000-0000-0000-0000-000000000002")
VERSION_ID_2 = UUID("00000000-0000-0000-0000-000000000003")
NOW = datetime(2024, 1, 1, 0, 0, 0)

MOCK_PROMPT_RESPONSE = PromptResponse(
    id=PROMPT_ID,
    name="smoke-test",
    status="active",
    active_version_id=None,
    created_at=NOW,
    updated_at=NOW,
)

MOCK_PROMPT_RESPONSE_WITH_CONTENT = PromptResponse(
    id=PROMPT_ID,
    name="smoke-test",
    status="active",
    active_version_id=None,
    created_at=NOW,
    updated_at=NOW,
    content="Hello, world!",
)

MOCK_VERSION_RESPONSE = PromptVersionResponse(
    id=VERSION_ID,
    prompt_id=PROMPT_ID,
    version_number=1,
    content="Hello, world!",
    created_at=NOW,
    is_active=False,
)

MOCK_DETAIL_RESPONSE = PromptDetailResponse(
    id=PROMPT_ID,
    name="smoke-test",
    status="active",
    active_version_id=None,
    created_at=NOW,
    updated_at=NOW,
    versions=[MOCK_VERSION_RESPONSE],
)

MOCK_DIFF_RESPONSE = VersionDiffResponse(
    prompt_id=PROMPT_ID,
    version_id_before=VERSION_ID,
    version_id_after=VERSION_ID_2,
    version_number_before=1,
    version_number_after=2,
    lines=[],
    has_changes=False,
)


@pytest.fixture
def mock_service() -> MagicMock:
    """A MagicMock whose async methods return structured response objects."""
    service = MagicMock()
    service.create_prompt = AsyncMock(return_value=MOCK_PROMPT_RESPONSE_WITH_CONTENT)
    service.add_version = AsyncMock(return_value=MOCK_VERSION_RESPONSE)
    service.update_content = AsyncMock(return_value=MOCK_VERSION_RESPONSE)
    service.activate_version = AsyncMock(return_value=MOCK_PROMPT_RESPONSE)
    service.get_prompt_by_id = AsyncMock(return_value=MOCK_DETAIL_RESPONSE)
    service.list_versions = AsyncMock(return_value=[MOCK_VERSION_RESPONSE])
    service.list_active_prompts = AsyncMock(return_value=[MOCK_PROMPT_RESPONSE])
    service.compare_versions = AsyncMock(return_value=MOCK_DIFF_RESPONSE)
    service.soft_delete_prompt = AsyncMock(return_value=MOCK_PROMPT_RESPONSE)
    service.list_deleted_prompts = AsyncMock(return_value=[MOCK_PROMPT_RESPONSE])
    service.recover_prompt = AsyncMock(return_value=MOCK_PROMPT_RESPONSE)
    return service


@pytest.fixture
def test_client(mock_service: MagicMock) -> TestClient:
    """FastAPI test app with mocked PromptService injected into app.state."""
    app = FastAPI()
    app.include_router(router)
    app.add_exception_handler(BaseAppException, app_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
    app.state.prompt_service = mock_service
    return TestClient(app, raise_server_exceptions=False)
