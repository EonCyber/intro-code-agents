import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from utils.error_handlers import app_exception_handler, generic_exception_handler
from utils.exceptions import BaseAppException, PromptNotFoundException


@pytest.fixture
def error_app() -> TestClient:
    app = FastAPI()
    app.add_exception_handler(BaseAppException, app_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    @app.get("/not-found")
    async def _not_found():
        raise PromptNotFoundException("p-1")

    @app.get("/custom")
    async def _custom():
        raise BaseAppException(
            message="custom error",
            error_code="CUSTOM",
            http_status=418,
            details={"hint": "teapot"},
        )

    @app.get("/crash")
    async def _crash():
        raise RuntimeError("unexpected crash")

    return TestClient(app, raise_server_exceptions=False)


def test_app_exception_handler_returns_structured_json(error_app: TestClient):
    response = error_app.get("/not-found")
    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "PROMPT_NOT_FOUND"
    assert "p-1" in body["error"]["message"]
    assert "details" in body["error"]


def test_app_exception_handler_custom_status(error_app: TestClient):
    response = error_app.get("/custom")
    assert response.status_code == 418
    body = response.json()
    assert body["error"]["code"] == "CUSTOM"
    assert body["error"]["details"] == {"hint": "teapot"}


def test_generic_exception_handler_returns_500(error_app: TestClient):
    response = error_app.get("/crash")
    assert response.status_code == 500
    body = response.json()
    assert body["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert "stack" not in response.text
