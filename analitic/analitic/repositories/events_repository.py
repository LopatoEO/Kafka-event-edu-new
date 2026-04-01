from aiochclient import ChClient
from datetime import datetime

class EventRepository:
    def __init__(self, client: ChClient):
        self.client = client



    async def get_events(self, user_id: int,
                            event_type: str,
                            event_time_from: datetime,
                            event_time_to: datetime):
        
        from_str = event_time_from.isoformat() if isinstance(event_time_from, datetime) else event_time_from
        to_str = event_time_to.isoformat() if isinstance(event_time_to, datetime) else event_time_to
        
        query = f"""
        SELECT *
        FROM kafka_events.events
        WHERE ts BETWEEN parseDateTime64BestEffort('{from_str}', 6) AND parseDateTime64BestEffort('{to_str}', 6)
        """

        if user_id is not None:
            query += f" AND user_id = {user_id}"

        if event_type is not None:
            escaped_event_type = str(event_type).replace("'", "''")
            query += f" AND type = '{escaped_event_type}'"

        query += " ORDER BY ts DESC"
        return await self.client.fetch(query)                        
