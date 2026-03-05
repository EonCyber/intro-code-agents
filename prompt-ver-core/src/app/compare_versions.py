from src.app.dtos import CompareVersionsQuery, DiffLineResponse, VersionDiffResponse
from src.app.exceptions import PromptNotFoundException
from src.domain.diff import VersionDiffer
from src.domain.exceptions import VersionNotFoundException
from src.ports.unit_of_work import UnitOfWork


class CompareVersionsUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(self, query: CompareVersionsQuery) -> VersionDiffResponse:
        async with self._uow:
            prompt = await self._uow.prompts.get_by_id(query.prompt_id)
            if prompt is None:
                raise PromptNotFoundException(query.prompt_id)
            await self._uow.commit()

        version_before = next(
            (v for v in prompt._versions if v.id == query.version_id_before), None
        )
        if version_before is None:
            raise VersionNotFoundException(query.version_id_before, query.prompt_id)

        version_after = next(
            (v for v in prompt._versions if v.id == query.version_id_after), None
        )
        if version_after is None:
            raise VersionNotFoundException(query.version_id_after, query.prompt_id)

        diff = VersionDiffer().compare(version_before, version_after)

        return VersionDiffResponse(
            prompt_id=diff.prompt_id,
            version_id_before=diff.version_id_before,
            version_id_after=diff.version_id_after,
            version_number_before=diff.version_number_before,
            version_number_after=diff.version_number_after,
            lines=tuple(
                DiffLineResponse(
                    kind=line.kind.value,
                    content=line.content,
                    line_number_before=line.line_number_before,
                    line_number_after=line.line_number_after,
                )
                for line in diff.lines
            ),
            has_changes=diff.has_changes,
        )
