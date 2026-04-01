from aiochclient import ChClient
from datetime import datetime

class EventRepository:
    def __init__(self, client: ChClient):
        self.client = client



    async def insert_events(self, events: list[dict]):
        if not events:
            return

        query = "INSERT INTO kafka_events.events (user_id, type, value, ts) VALUES"

        data = [
            (
                e["user_id"],
                e['event'],
                e['value'],
                e.get("received_at").replace("Z", "").replace("T", " ")
            )
            for e in events
        ]
        print(data)

        await self.client.execute(query, *data)