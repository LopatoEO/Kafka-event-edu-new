from aiochclient import ChClient
from datetime import datetime


from src.repositories.events_repository_interface import IEventRepository   
from src.schemas.events import EventListResponseDTO, EventResponseDTO, EventsSearchParamsDTO

class EventRepository(IEventRepository):
    def __init__(self, client: ChClient) -> None:
        self.client = client



    async def get_events(self,search_params :EventsSearchParamsDTO) -> EventListResponseDTO:
        
        from_str = search_params.date_from.isoformat() if isinstance(search_params.date_from, datetime) else search_params.date_from
        to_str = search_params.date_to.isoformat() if isinstance(search_params.date_to, datetime) else search_params.date_to
        
        query = f"""
        SELECT *
        FROM kafka_events.events
        WHERE ts BETWEEN parseDateTime64BestEffort('{from_str}', 6) AND parseDateTime64BestEffort('{to_str}', 6)
        """

        if search_params.user_id is not None:
            query += f" AND user_id = {search_params.user_id}"

        if search_params.event is not None:
            escaped_event_type = str(search_params.event).replace("'", "''")
            query += f" AND type = '{escaped_event_type}'"

        query += " ORDER BY ts DESC"

        events = await self.client.fetch(query)

        
        return EventListResponseDTO(events=[EventResponseDTO(**event) for event in events])                      
