import json
from typing import Any


def serialize(payload: Any) -> bytes:
    """Serialize a Python object to UTF-8 encoded JSON bytes."""
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def deserialize(data: bytes) -> Any:
    """Deserialize UTF-8 encoded JSON bytes to a Python object."""
    return json.loads(data.decode("utf-8"))
