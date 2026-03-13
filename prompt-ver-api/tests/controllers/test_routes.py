import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock


# ---------------------------------------------------------------------------
# POST /prompts
# ---------------------------------------------------------------------------

def test_create_prompt_calls_service(test_client: TestClient, mock_service: MagicMock):
    response = test_client.post("/prompts/", json={"name": "smoke-test", "content": "Hello, world!"})
    assert response.status_code == 200
    mock_service.create_prompt.assert_awaited_once()
    req = mock_service.create_prompt.call_args[0][0]
    assert req.name == "smoke-test"
    assert req.content == "Hello, world!"


def test_create_prompt_returns_prompt_response(test_client: TestClient, mock_service: MagicMock):
    response = test_client.post("/prompts/", json={"name": "smoke-test", "content": "Hello, world!"})
    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert body["name"] == "smoke-test"
    assert body["status"] == "active"
    assert "created_at" in body
    assert "updated_at" in body
    assert body["content"] == "Hello, world!"


# ---------------------------------------------------------------------------
# POST /prompts/{prompt_id}/versions
# ---------------------------------------------------------------------------

def test_add_version_calls_service(test_client: TestClient, mock_service: MagicMock):
    response = test_client.post(
        "/prompts/p-1/versions", json={"content": "Hello, world!"}
    )
    assert response.status_code == 200
    mock_service.add_version.assert_awaited_once()
    req = mock_service.add_version.call_args[0][0]
    assert req.prompt_id == "p-1"
    assert req.content == "Hello, world!"


def test_add_version_returns_version_response(test_client: TestClient, mock_service: MagicMock):
    response = test_client.post(
        "/prompts/p-1/versions", json={"content": "Hello, world!"}
    )
    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert "prompt_id" in body
    assert body["version_number"] == 1
    assert body["content"] == "Hello, world!"
    assert "is_active" in body


# ---------------------------------------------------------------------------
# PUT /prompts/{prompt_id}/content
# ---------------------------------------------------------------------------

def test_update_content_calls_service(test_client: TestClient, mock_service: MagicMock):
    response = test_client.put(
        "/prompts/p-1/content", json={"content": "Updated content"}
    )
    assert response.status_code == 200
    mock_service.update_content.assert_awaited_once()
    req = mock_service.update_content.call_args[0][0]
    assert req.prompt_id == "p-1"
    assert req.content == "Updated content"


def test_update_content_returns_version_response(test_client: TestClient, mock_service: MagicMock):
    response = test_client.put(
        "/prompts/p-1/content", json={"content": "Updated content"}
    )
    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert "prompt_id" in body
    assert "version_number" in body
    assert "content" in body


# ---------------------------------------------------------------------------
# POST /prompts/{prompt_id}/activate
# ---------------------------------------------------------------------------

def test_activate_version_calls_service(test_client: TestClient, mock_service: MagicMock):
    response = test_client.post(
        "/prompts/p-1/activate", json={"version_id": "v-1"}
    )
    assert response.status_code == 200
    mock_service.activate_version.assert_awaited_once()
    req = mock_service.activate_version.call_args[0][0]
    assert req.prompt_id == "p-1"
    assert req.version_id == "v-1"


def test_activate_version_returns_prompt_response(test_client: TestClient, mock_service: MagicMock):
    response = test_client.post(
        "/prompts/p-1/activate", json={"version_id": "v-1"}
    )
    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert "name" in body
    assert "status" in body


# ---------------------------------------------------------------------------
# GET /prompts/active
# ---------------------------------------------------------------------------

def test_list_active_prompts_calls_service(
    test_client: TestClient, mock_service: MagicMock
):
    response = test_client.get("/prompts/active")
    assert response.status_code == 200
    mock_service.list_active_prompts.assert_awaited_once()


def test_list_active_prompts_returns_array(
    test_client: TestClient, mock_service: MagicMock
):
    response = test_client.get("/prompts/active")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) > 0
    assert "id" in body[0]
    assert "name" in body[0]


# ---------------------------------------------------------------------------
# GET /prompts/deleted
# ---------------------------------------------------------------------------

def test_list_deleted_prompts_calls_service(
    test_client: TestClient, mock_service: MagicMock
):
    response = test_client.get("/prompts/deleted")
    assert response.status_code == 200
    mock_service.list_deleted_prompts.assert_awaited_once()


def test_list_deleted_prompts_returns_array(
    test_client: TestClient, mock_service: MagicMock
):
    response = test_client.get("/prompts/deleted")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert "id" in body[0]


# ---------------------------------------------------------------------------
# GET /prompts/{prompt_id}
# ---------------------------------------------------------------------------

def test_get_prompt_by_id_calls_service(
    test_client: TestClient, mock_service: MagicMock
):
    response = test_client.get("/prompts/p-1")
    assert response.status_code == 200
    mock_service.get_prompt_by_id.assert_awaited_once()
    req = mock_service.get_prompt_by_id.call_args[0][0]
    assert req.prompt_id == "p-1"


def test_get_prompt_by_id_returns_detail_response(
    test_client: TestClient, mock_service: MagicMock
):
    response = test_client.get("/prompts/p-1")
    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert "versions" in body
    assert isinstance(body["versions"], list)


# ---------------------------------------------------------------------------
# GET /prompts/{prompt_id}/versions
# ---------------------------------------------------------------------------

def test_list_versions_calls_service(test_client: TestClient, mock_service: MagicMock):
    response = test_client.get("/prompts/p-1/versions")
    assert response.status_code == 200
    mock_service.list_versions.assert_awaited_once()
    req = mock_service.list_versions.call_args[0][0]
    assert req.prompt_id == "p-1"


def test_list_versions_returns_array(test_client: TestClient, mock_service: MagicMock):
    response = test_client.get("/prompts/p-1/versions")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert "version_number" in body[0]


# ---------------------------------------------------------------------------
# POST /prompts/{prompt_id}/compare
# ---------------------------------------------------------------------------

def test_compare_versions_calls_service(
    test_client: TestClient, mock_service: MagicMock
):
    response = test_client.post(
        "/prompts/p-1/compare",
        json={"version_id_before": "v-1", "version_id_after": "v-2"},
    )
    assert response.status_code == 200
    mock_service.compare_versions.assert_awaited_once()
    req = mock_service.compare_versions.call_args[0][0]
    assert req.prompt_id == "p-1"
    assert req.version_id_before == "v-1"
    assert req.version_id_after == "v-2"


def test_compare_versions_returns_diff_response(
    test_client: TestClient, mock_service: MagicMock
):
    response = test_client.post(
        "/prompts/p-1/compare",
        json={"version_id_before": "v-1", "version_id_after": "v-2"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "prompt_id" in body
    assert "version_id_before" in body
    assert "version_id_after" in body
    assert "lines" in body
    assert "has_changes" in body


# ---------------------------------------------------------------------------
# DELETE /prompts/{prompt_id}
# ---------------------------------------------------------------------------

def test_soft_delete_prompt_calls_service(
    test_client: TestClient, mock_service: MagicMock
):
    response = test_client.delete("/prompts/p-1")
    assert response.status_code == 200
    mock_service.soft_delete_prompt.assert_awaited_once()
    req = mock_service.soft_delete_prompt.call_args[0][0]
    assert req.prompt_id == "p-1"


def test_soft_delete_prompt_returns_prompt_response(
    test_client: TestClient, mock_service: MagicMock
):
    response = test_client.delete("/prompts/p-1")
    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert "status" in body


# ---------------------------------------------------------------------------
# POST /prompts/{prompt_id}/recover
# ---------------------------------------------------------------------------

def test_recover_prompt_calls_service(test_client: TestClient, mock_service: MagicMock):
    response = test_client.post("/prompts/p-1/recover")
    assert response.status_code == 200
    mock_service.recover_prompt.assert_awaited_once()
    req = mock_service.recover_prompt.call_args[0][0]
    assert req.prompt_id == "p-1"


def test_recover_prompt_returns_prompt_response(test_client: TestClient, mock_service: MagicMock):
    response = test_client.post("/prompts/p-1/recover")
    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert "name" in body
    assert "status" in body
