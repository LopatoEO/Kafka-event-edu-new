from src.repositories.events_repository_interface import IEventRepository

from src.schemas.events import EventListResponseDTO, EventsSearchParamsDTO



class EventsService:
    def __init__(self, repository: IEventRepository):
        self._repo = repository

    async def get_events(self, search_params: EventsSearchParamsDTO) -> EventListResponseDTO:
        return await self._repo.get_events(search_params)