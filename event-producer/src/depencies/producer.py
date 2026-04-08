from aiokafka import AIOKafkaProducer
from typing import AsyncGenerator
from dishka import Provider, provide, Scope
from src.settings import settings
from src.service.event_service import EventService


class KafkaProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_kafka(self) -> AsyncGenerator[AIOKafkaProducer, None]:
        producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS.split(","))
        await producer.start()
        try:
            yield producer
        finally:
            await producer.stop()

class EventServiceProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def get_service(self, client: AIOKafkaProducer) -> EventService:
        return EventService(client)
