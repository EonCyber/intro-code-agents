import pytest
from unittest.mock import AsyncMock, MagicMock

from messaging.nats_publisher import NATSPublisher
from models.prompt_models import (
    ActivateVersionRequest,
    AddVersionRequest,
    CompareVersionsRequest,
    CreatePromptRequest,
    GetPromptByIdRequest,
    ListActivePromptsRequest,
    ListDeletedPromptsRequest,
    ListVersionsRequest,
    PromptDetailResponse,
    PromptResponse,
    PromptVersionResponse,
    RecoverPromptRequest,
    SoftDeletePromptRequest,
    UpdateContentRequest,
    VersionDiffResponse,
)
from services.prompt_service import PromptService

PROMPT_DATA = {
    "id": "00000000-0000-0000-0000-000000000001",
    "name": "my-prompt",
    "status": "active",
    "active_version_id": None,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00",
}

VERSION_DATA = {
    "id": "00000000-0000-0000-0000-000000000002",
    "prompt_id": "00000000-0000-0000-0000-000000000001",
    "version_number": 1,
    "content": "Hello world",
    "created_at": "2024-01-01T00:00:00",
    "is_active": False,
}

DIFF_DATA = {
    "prompt_id": "00000000-0000-0000-0000-000000000001",
    "version_id_before": "00000000-0000-0000-0000-000000000002",
    "version_id_after": "00000000-0000-0000-0000-000000000003",
    "version_number_before": 1,
    "version_number_after": 2,
    "lines": [],
    "has_changes": False,
}


@pytest.fixture
def mock_publisher() -> MagicMock:
    publisher = MagicMock(spec=NATSPublisher)
    publisher.request = AsyncMock()
    return publisher


@pytest.fixture
def service(mock_publisher) -> PromptService:
    return PromptService(mock_publisher)


async def test_create_prompt_requests_correct_event(service, mock_publisher):
    mock_publisher.request.return_value = {**PROMPT_DATA, "content": "v1"}
    req = CreatePromptRequest(name="my-prompt", content="Hello world")
    result = await service.create_prompt(req)

    mock_publisher.request.assert_awaited_once_with(
        "prompts.v1.commands.create_prompt",
        {"name": "my-prompt", "content": "Hello world"},
    )
    assert isinstance(result, PromptResponse)
    assert result.name == "my-prompt"


async def test_add_version_requests_correct_event(service, mock_publisher):
    mock_publisher.request.return_value = VERSION_DATA
    req = AddVersionRequest(prompt_id="p-1", content="Hello world")
    result = await service.add_version(req)

    mock_publisher.request.assert_awaited_once_with(
        "prompts.v1.commands.add_version",
        {"prompt_id": "p-1", "content": "Hello world"},
    )
    assert isinstance(result, PromptVersionResponse)
    assert result.content == "Hello world"


async def test_update_content_requests_correct_event(service, mock_publisher):
    mock_publisher.request.return_value = {**VERSION_DATA, "content": "Updated"}
    req = UpdateContentRequest(prompt_id="p-1", content="Updated")
    result = await service.update_content(req)

    mock_publisher.request.assert_awaited_once_with(
        "prompts.v1.commands.update_content",
        {"prompt_id": "p-1", "content": "Updated"},
    )
    assert isinstance(result, PromptVersionResponse)
    assert result.content == "Updated"


async def test_activate_version_requests_correct_event(service, mock_publisher):
    mock_publisher.request.return_value = PROMPT_DATA
    req = ActivateVersionRequest(prompt_id="p-1", version_id="v-1")
    result = await service.activate_version(req)

    mock_publisher.request.assert_awaited_once_with(
        "prompts.v1.commands.activate_version",
        {"prompt_id": "p-1", "version_id": "v-1"},
    )
    assert isinstance(result, PromptResponse)


async def test_get_prompt_by_id_requests_correct_event(service, mock_publisher):
    mock_publisher.request.return_value = {**PROMPT_DATA, "versions": []}
    req = GetPromptByIdRequest(prompt_id="p-1")
    result = await service.get_prompt_by_id(req)

    mock_publisher.request.assert_awaited_once_with(
        "prompts.v1.queries.get_prompt_by_id",
        {"prompt_id": "p-1"},
    )
    assert isinstance(result, PromptDetailResponse)
    assert result.versions == []


async def test_list_versions_requests_correct_event(service, mock_publisher):
    mock_publisher.request.return_value = [VERSION_DATA]
    req = ListVersionsRequest(prompt_id="p-1")
    result = await service.list_versions(req)

    mock_publisher.request.assert_awaited_once_with(
        "prompts.v1.queries.list_versions",
        {"prompt_id": "p-1"},
    )
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], PromptVersionResponse)


async def test_list_active_prompts_requests_correct_event(service, mock_publisher):
    mock_publisher.request.return_value = [PROMPT_DATA]
    req = ListActivePromptsRequest()
    result = await service.list_active_prompts(req)

    mock_publisher.request.assert_awaited_once_with(
        "prompts.v1.queries.list_active_prompts",
        {},
    )
    assert isinstance(result, list)
    assert isinstance(result[0], PromptResponse)


async def test_compare_versions_requests_correct_event(service, mock_publisher):
    mock_publisher.request.return_value = DIFF_DATA
    req = CompareVersionsRequest(
        prompt_id="p-1", version_id_before="v-1", version_id_after="v-2"
    )
    result = await service.compare_versions(req)

    mock_publisher.request.assert_awaited_once_with(
        "prompts.v1.queries.compare_versions",
        {"prompt_id": "p-1", "version_id_before": "v-1", "version_id_after": "v-2"},
    )
    assert isinstance(result, VersionDiffResponse)
    assert result.has_changes is False


async def test_soft_delete_prompt_requests_correct_event(service, mock_publisher):
    mock_publisher.request.return_value = PROMPT_DATA
    req = SoftDeletePromptRequest(prompt_id="p-1")
    result = await service.soft_delete_prompt(req)

    mock_publisher.request.assert_awaited_once_with(
        "prompts.v1.commands.soft_delete_prompt",
        {"prompt_id": "p-1"},
    )
    assert isinstance(result, PromptResponse)


async def test_list_deleted_prompts_requests_correct_event(service, mock_publisher):
    mock_publisher.request.return_value = [PROMPT_DATA]
    req = ListDeletedPromptsRequest()
    result = await service.list_deleted_prompts(req)

    mock_publisher.request.assert_awaited_once_with(
        "prompts.v1.queries.list_deleted_prompts",
        {},
    )
    assert isinstance(result, list)
    assert isinstance(result[0], PromptResponse)


async def test_recover_prompt_requests_correct_event(service, mock_publisher):
    mock_publisher.request.return_value = PROMPT_DATA
    req = RecoverPromptRequest(prompt_id="p-1")
    result = await service.recover_prompt(req)

    mock_publisher.request.assert_awaited_once_with(
        "prompts.v1.commands.recover_prompt",
        {"prompt_id": "p-1"},
    )
    assert isinstance(result, PromptResponse)
