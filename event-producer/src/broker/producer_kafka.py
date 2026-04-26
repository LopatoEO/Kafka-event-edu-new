from aiokafka import AIOKafkaProducer
from fastapi.encoders import jsonable_encoder
from src.models.event import EventDTO
from src.broker.producer_interface import IEventProducer
from src.settings.kafka import KafkaSettings

class KafkaProducer(IEventProducer):
    def __init__(self, settings: KafkaSettings) -> None:
        self.producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
        self.topic = settings.KAFKA_TOPIC

    async def post_event(self, event: EventDTO) -> None:
        await self.producer.send_and_wait(self.topic,
            jsonable_encoder(event).encode('utf-8'),
            key=str(event.user_id).encode('utf-8'))