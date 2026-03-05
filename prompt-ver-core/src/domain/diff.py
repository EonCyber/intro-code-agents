from dataclasses import dataclass
from difflib import SequenceMatcher
from enum import Enum
from uuid import UUID

from src.domain.prompt_version import PromptVersion


class DiffLineKind(str, Enum):
    ADDED = "ADDED"
    REMOVED = "REMOVED"
    EQUAL = "EQUAL"


@dataclass(frozen=True)
class DiffLine:
    kind: DiffLineKind
    content: str
    line_number_before: int | None
    line_number_after: int | None


@dataclass(frozen=True)
class VersionDiff:
    prompt_id: UUID
    version_id_before: UUID
    version_id_after: UUID
    version_number_before: int
    version_number_after: int
    lines: tuple[DiffLine, ...]

    @property
    def has_changes(self) -> bool:
        return any(line.kind != DiffLineKind.EQUAL for line in self.lines)


class VersionDiffer:
    def compare(self, before: PromptVersion, after: PromptVersion) -> VersionDiff:
        before_lines = before.content.value.splitlines()
        after_lines = after.content.value.splitlines()

        matcher = SequenceMatcher(None, before_lines, after_lines, autojunk=False)
        diff_lines: list[DiffLine] = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                for k, line in enumerate(before_lines[i1:i2]):
                    diff_lines.append(DiffLine(
                        kind=DiffLineKind.EQUAL,
                        content=line,
                        line_number_before=i1 + k + 1,
                        line_number_after=j1 + k + 1,
                    ))
            elif tag == "replace":
                for k, line in enumerate(before_lines[i1:i2]):
                    diff_lines.append(DiffLine(
                        kind=DiffLineKind.REMOVED,
                        content=line,
                        line_number_before=i1 + k + 1,
                        line_number_after=None,
                    ))
                for k, line in enumerate(after_lines[j1:j2]):
                    diff_lines.append(DiffLine(
                        kind=DiffLineKind.ADDED,
                        content=line,
                        line_number_before=None,
                        line_number_after=j1 + k + 1,
                    ))
            elif tag == "delete":
                for k, line in enumerate(before_lines[i1:i2]):
                    diff_lines.append(DiffLine(
                        kind=DiffLineKind.REMOVED,
                        content=line,
                        line_number_before=i1 + k + 1,
                        line_number_after=None,
                    ))
            elif tag == "insert":
                for k, line in enumerate(after_lines[j1:j2]):
                    diff_lines.append(DiffLine(
                        kind=DiffLineKind.ADDED,
                        content=line,
                        line_number_before=None,
                        line_number_after=j1 + k + 1,
                    ))

        return VersionDiff(
            prompt_id=before.prompt_id,
            version_id_before=before.id,
            version_id_after=after.id,
            version_number_before=before.version_number.value,
            version_number_after=after.version_number.value,
            lines=tuple(diff_lines),
        )
