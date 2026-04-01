from ..repositories.events_repository import EventRepository
from aiochclient import ChClient

class EventsService:
    def __init__(self, client: ChClient):
        self.repo = EventRepository(client)

    async def get_events(self, user_id: int, event_type: str, event_time_from: str, event_time_to: str):
        res = await self.repo.get_events(user_id, event_type, event_time_from, event_time_to)
        return res