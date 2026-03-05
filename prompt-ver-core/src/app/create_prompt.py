from src.app.dtos import CreatePromptCommand, PromptResponse
from src.domain.prompt import Prompt
from src.domain.value_objects import PromptName
from src.ports.event_publisher import EventPublisher
from src.ports.unit_of_work import UnitOfWork


class CreatePromptUseCase:
    def __init__(self, uow: UnitOfWork, publisher: EventPublisher):
        self._uow = uow
        self._publisher = publisher

    async def execute(self, command: CreatePromptCommand) -> PromptResponse:
        name = PromptName(command.name)
        prompt = Prompt.create(name)
        async with self._uow:
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
