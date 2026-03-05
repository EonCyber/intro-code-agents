from src.app.dtos import PromptResponse
from src.domain.enums import PromptStatus
from src.ports.unit_of_work import UnitOfWork


class ListActivePromptsUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(self) -> list[PromptResponse]:
        async with self._uow:
            prompts = await self._uow.prompts.list_by_status(PromptStatus.ACTIVE)
            await self._uow.commit()
        return [
            PromptResponse(
                id=p.id,
                name=p.name.value,
                status=p.status.value,
                active_version_id=p.active_version_id,
                created_at=p.created_at,
                updated_at=p.updated_at,
            )
            for p in prompts
        ]
