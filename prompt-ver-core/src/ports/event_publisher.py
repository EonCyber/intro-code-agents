from abc import ABC, abstractmethod

from src.domain.events import DomainEvent


class EventPublisher(ABC):
    @abstractmethod
    async def publish(self, events: list[DomainEvent]) -> None: ...
