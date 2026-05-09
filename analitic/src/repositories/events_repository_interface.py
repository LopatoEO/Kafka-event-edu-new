from abc import ABC, abstractmethod

from src.schemas.events import EventListResponseDTO, EventsSearchParamsDTO

class IEventRepository(ABC):

    @abstractmethod
    async def get_events(self, search_params :EventsSearchParamsDTO) -> EventListResponseDTO:
        pass    