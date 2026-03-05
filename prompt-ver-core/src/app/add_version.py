from src.app.dtos import AddVersionCommand, PromptVersionResponse
from src.app.exceptions import PromptNotFoundException
from src.domain.value_objects import PromptContent
from src.ports.event_publisher import EventPublisher
from src.ports.unit_of_work import UnitOfWork


class AddVersionUseCase:
    def __init__(self, uow: UnitOfWork, publisher: EventPublisher):
        self._uow = uow
        self._publisher = publisher

    async def execute(self, command: AddVersionCommand) -> PromptVersionResponse:
        content = PromptContent(command.content)
        async with self._uow:
            prompt = await self._uow.prompts.get_by_id(command.prompt_id)
            if prompt is None:
                raise PromptNotFoundException(command.prompt_id)
            version = prompt.add_version(content)
            await self._uow.prompts.save(prompt)
            await self._uow.commit()
            events = prompt.collect_events()
        await self._publisher.publish(events)
        return PromptVersionResponse(
            id=version.id,
            prompt_id=version.prompt_id,
            version_number=version.version_number.value,
            content=version.content.value,
            created_at=version.created_at,
            is_active=version.is_active,
        )
