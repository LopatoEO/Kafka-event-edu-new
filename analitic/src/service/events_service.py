from datetime import datetime
from aiochclient import ChClient, Record
from src.repositories.events_repository import EventRepository
from src.schemas.events import EventsResponseDTO, EventDTO



class EventsService:
    def __init__(self, client: ChClient):
        self.repo = EventRepository(client)

    async def get_events(self,
                         user_id: int | None,
                         event_type: str | None,
                         event_time_from: datetime,
                         event_time_to: datetime) -> EventsResponseDTO:
        events = await self.repo.get_events(user_id, event_type, event_time_from, event_time_to)
        return EventsResponseDTO(events=[EventDTO(**event) for event in events])