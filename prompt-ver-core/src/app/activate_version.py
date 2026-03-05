from src.app.dtos import ActivateVersionCommand, PromptResponse
from src.app.exceptions import PromptNotFoundException
from src.ports.event_publisher import EventPublisher
from src.ports.unit_of_work import UnitOfWork


class ActivateVersionUseCase:
    def __init__(self, uow: UnitOfWork, publisher: EventPublisher):
        self._uow = uow
        self._publisher = publisher

    async def execute(self, command: ActivateVersionCommand) -> PromptResponse:
        async with self._uow:
            prompt = await self._uow.prompts.get_by_id(command.prompt_id)
            if prompt is None:
                raise PromptNotFoundException(command.prompt_id)
            prompt.activate_version(command.version_id)
            await self._uow.prompts.save(prompt)
            await self._uow.commit()
            events = prompt.collect_events()
        await self._publisher.publish(events)
        return PromptResponse(
            id=prompt.id,
            name=prompt.name.value,
            status=prompt.status.value,
            active_version_id=prompt.active_version_id,
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,
        )
