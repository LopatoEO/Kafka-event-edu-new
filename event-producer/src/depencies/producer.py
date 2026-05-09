from dishka import Provider, provide, Scope
from src.services.event_service import EventService
from src.broker.producer_kafka import KafkaProducer
from src.settings.kafka import KafkaSettings
from src.settings.settings import app_settings


class KafkaSettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_kafka_settings(self) -> KafkaSettings:
        return app_settings.KAFKA_SETTINGS

class KafkaProducerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_producer(self, settings: KafkaSettings) -> KafkaProducer:
        return KafkaProducer(settings)

class EventServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_service(self, producer: KafkaProducer) -> EventService:
        return EventService(producer=producer)
