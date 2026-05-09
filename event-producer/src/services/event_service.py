from src.models.event import EventDTO

from src.broker.producer_interface import IEventProducer

class EventService:
    def __init__(self, producer: IEventProducer) -> None:
        self.producer = producer

    async def send_event(self, event: EventDTO) -> None:
        await self.producer.post_event(event)