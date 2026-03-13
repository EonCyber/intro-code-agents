from utils.json_utils import deserialize, serialize


def test_serialize_simple_dict():
    result = serialize({"name": "test"})
    assert result == b'{"name": "test"}'


def test_serialize_empty_dict():
    assert serialize({}) == b"{}"


def test_serialize_nested():
    data = {"prompt_id": "p-1", "content": "hello"}
    result = serialize(data)
    assert b"prompt_id" in result
    assert b"p-1" in result


def test_serialize_returns_bytes():
    assert isinstance(serialize({"k": "v"}), bytes)


def test_deserialize_bytes_to_dict():
    data = b'{"name": "test"}'
    result = deserialize(data)
    assert result == {"name": "test"}


def test_deserialize_empty():
    assert deserialize(b"{}") == {}


def test_serialize_deserialize_roundtrip():
    original = {"prompt_id": "abc", "version_id": "xyz", "active": True}
    assert deserialize(serialize(original)) == original


def test_serialize_handles_non_ascii():
    result = serialize({"msg": "não encontrado"})
    assert "não encontrado".encode("utf-8") in result
