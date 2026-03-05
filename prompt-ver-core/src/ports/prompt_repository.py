from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.enums import PromptStatus
from src.domain.prompt import Prompt


class PromptRepository(ABC):
    @abstractmethod
    async def get_by_id(self, prompt_id: UUID) -> Prompt | None: ...

    @abstractmethod
    async def save(self, prompt: Prompt) -> None: ...

    @abstractmethod
    async def list_by_status(self, status: PromptStatus) -> list[Prompt]: ...
