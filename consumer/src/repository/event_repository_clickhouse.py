from datetime import datetime

from clickhouse_connect.driver import Client

from src.repository.event_repository_interface import IEventRepository


class EventRepository(IEventRepository):
    def __init__(self, client: Client):
        self.client = client

    def insert_events(self, events: list[dict]) -> None:
        if not events:
            return

        data = [
            (
                e["user_id"],
                e["event"],
                str(e["value"]),
                datetime.fromisoformat(e["received_at"].replace("Z", "+00:00")),
            )
            for e in events
        ]

        self.client.insert(
            "kafka_events.events",
            data,
            column_names=["user_id", "type", "value", "ts"],
        )
