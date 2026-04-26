from abc import ABC, abstractmethod
from src.models.event import EventDTO

class IEventProducer(ABC):

    @abstractmethod
    async def post_event(self, event: EventDTO) -> None:   
        pass