import pytest

from utils.exceptions import (
    BaseAppException,
    InvalidVersionComparisonException,
    NATSPublishException,
    PromptAlreadyDeletedException,
    PromptNotFoundException,
    VersionNotFoundException,
)


def test_base_app_exception_fields():
    exc = BaseAppException(
        message="something went wrong",
        error_code="GENERIC",
        http_status=400,
        details={"k": "v"},
    )
    assert exc.message == "something went wrong"
    assert exc.error_code == "GENERIC"
    assert exc.http_status == 400
    assert exc.details == {"k": "v"}
    assert str(exc) == "something went wrong"


def test_base_app_exception_default_details():
    exc = BaseAppException(message="err", error_code="ERR")
    assert exc.details == {}
    assert exc.http_status == 400


def test_prompt_not_found():
    exc = PromptNotFoundException("p-42")
    assert exc.http_status == 404
    assert exc.error_code == "PROMPT_NOT_FOUND"
    assert "p-42" in exc.message


def test_version_not_found():
    exc = VersionNotFoundException("v-99")
    assert exc.http_status == 404
    assert exc.error_code == "VERSION_NOT_FOUND"
    assert "v-99" in exc.message


def test_prompt_already_deleted():
    exc = PromptAlreadyDeletedException("p-1")
    assert exc.http_status == 409
    assert exc.error_code == "PROMPT_ALREADY_DELETED"
    assert "p-1" in exc.message


def test_invalid_version_comparison_with_detail():
    exc = InvalidVersionComparisonException("versions must differ")
    assert exc.http_status == 422
    assert exc.error_code == "INVALID_VERSION_COMPARISON"
    assert exc.details == {"detail": "versions must differ"}


def test_invalid_version_comparison_no_detail():
    exc = InvalidVersionComparisonException()
    assert exc.details == {}


def test_nats_publish_exception_with_cause():
    exc = NATSPublishException("timeout")
    assert exc.http_status == 502
    assert exc.error_code == "NATS_PUBLISH_ERROR"
    assert exc.details == {"cause": "timeout"}


def test_nats_publish_exception_no_cause():
    exc = NATSPublishException()
    assert exc.details == {}


def test_exceptions_are_subclass_of_base():
    for cls, args in [
        (PromptNotFoundException, ("p-1",)),
        (VersionNotFoundException, ("v-1",)),
        (PromptAlreadyDeletedException, ("p-1",)),
        (InvalidVersionComparisonException, ()),
        (NATSPublishException, ()),
    ]:
        assert isinstance(cls(*args), BaseAppException)
