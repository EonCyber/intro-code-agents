import pytest
from unittest.mock import AsyncMock, MagicMock

from messaging.nats_publisher import NATSPublisher
from utils.exceptions import NATSPublishException, NATSRequestException


@pytest.fixture
def mock_nc():
    nc = AsyncMock()
    nc.publish = AsyncMock()
    nc.request = AsyncMock()
    return nc


@pytest.fixture
def publisher(mock_nc) -> NATSPublisher:
    return NATSPublisher(mock_nc)


async def test_publish_sends_json_bytes(publisher: NATSPublisher, mock_nc):
    await publisher.publish("test.subject", {"key": "value"})

    mock_nc.publish.assert_awaited_once()
    subject, data = mock_nc.publish.call_args[0]
    assert subject == "test.subject"
    assert data == b'{"key": "value"}'


async def test_publish_empty_payload(publisher: NATSPublisher, mock_nc):
    await publisher.publish("test.empty", {})

    _, data = mock_nc.publish.call_args[0]
    assert data == b"{}"


async def test_publish_raises_nats_publish_exception_on_error(
    publisher: NATSPublisher, mock_nc
):
    mock_nc.publish.side_effect = Exception("connection refused")

    with pytest.raises(NATSPublishException) as exc_info:
        await publisher.publish("fail.subject", {"k": "v"})

    assert exc_info.value.error_code == "NATS_PUBLISH_ERROR"
    assert exc_info.value.http_status == 502
    assert "connection refused" in exc_info.value.details["cause"]


async def test_request_sends_json_bytes_and_returns_deserialized(
    publisher: NATSPublisher, mock_nc
):
    mock_msg = MagicMock()
    mock_msg.data = b'{"id": "abc"}'
    mock_nc.request.return_value = mock_msg

    result = await publisher.request("test.subject", {"key": "value"})

    mock_nc.request.assert_awaited_once()
    subject, data = mock_nc.request.call_args[0]
    assert subject == "test.subject"
    assert data == b'{"key": "value"}'
    assert result == {"id": "abc"}


async def test_request_raises_nats_request_exception_on_error(
    publisher: NATSPublisher, mock_nc
):
    mock_nc.request.side_effect = Exception("timeout")

    with pytest.raises(NATSRequestException) as exc_info:
        await publisher.request("fail.subject", {"k": "v"})

    assert exc_info.value.error_code == "NATS_REQUEST_ERROR"
    assert exc_info.value.http_status == 502
    assert "timeout" in exc_info.value.details["cause"]
