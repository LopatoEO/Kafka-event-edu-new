from aiokafka import AIOKafkaProducer
from src.models.event import EventDTO

class EventService:
    def __init__(self, producer: AIOKafkaProducer) -> None:
        self.producer = producer

    async def send_event(self, topic: str, event: EventDTO) -> None:
        await self.producer.send_and_wait(topic,
                                          event.model_dump_json().encode('utf-8'),
                                          key=str(event.user_id).encode('utf-8'))