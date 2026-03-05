import re
from dataclasses import dataclass
from functools import total_ordering

from src.domain.exceptions import (
    InvalidPromptContentException,
    InvalidPromptNameException,
    InvalidVersionNumberException,
)

_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_\-]{0,127}$")


@dataclass(frozen=True)
class PromptContent:
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise InvalidPromptContentException("Prompt content must not be empty or whitespace")

    def truncated_preview(self, max_length: int = 80) -> str:
        if len(self.value) <= max_length:
            return self.value
        return self.value[:max_length] + "..."


@total_ordering
@dataclass(frozen=True)
class VersionNumber:
    value: int

    def __post_init__(self):
        if self.value < 1:
            raise InvalidVersionNumberException(f"Version number must be >= 1, got {self.value}")

    def next(self) -> "VersionNumber":
        return VersionNumber(self.value + 1)

    def __lt__(self, other: "VersionNumber") -> bool:
        return self.value < other.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VersionNumber):
            return NotImplemented
        return self.value == other.value


@dataclass(frozen=True)
class PromptName:
    value: str

    def __post_init__(self):
        if not _NAME_PATTERN.match(self.value):
            raise InvalidPromptNameException(
                f"Prompt name '{self.value}' must match pattern ^[a-z][a-z0-9_\\-]{{0,127}}$"
            )
