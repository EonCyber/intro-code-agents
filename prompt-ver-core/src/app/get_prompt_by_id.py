from src.app.dtos import GetPromptByIdQuery, PromptDetailResponse, PromptVersionResponse
from src.app.exceptions import PromptNotFoundException
from src.ports.unit_of_work import UnitOfWork


class GetPromptByIdUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(self, query: GetPromptByIdQuery) -> PromptDetailResponse:
        async with self._uow:
            prompt = await self._uow.prompts.get_by_id(query.prompt_id)
            if prompt is None:
                raise PromptNotFoundException(query.prompt_id)
            await self._uow.commit()
        versions = [
            PromptVersionResponse(
                id=v.id,
                prompt_id=v.prompt_id,
                version_number=v.version_number.value,
                content=v.content.value,
                created_at=v.created_at,
                is_active=v.is_active,
            )
            for v in sorted(prompt._versions, key=lambda v: v.version_number.value)
        ]
        return PromptDetailResponse(
            id=prompt.id,
            name=prompt.name.value,
            status=prompt.status.value,
            active_version_id=prompt.active_version_id,
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,
            versions=versions,
        )
