from collections.abc import Generator

from confluent_kafka import Consumer, Producer
from dishka import Provider, Scope, provide

from src.broker.consumer import KafkaConsumer
from src.broker.producer import KafkaProducer
from src.settings.kafka import KafkaSettings
from src.settings.settings import AppSettings, app_settings


class KafkaSettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_kafka_settings(self) -> KafkaSettings:
        return app_settings.KAFKA_SETTINGS

class AppSettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_app_settings(self) -> AppSettings:
        return app_settings

class KafkaProducerProvider(Provider):
    @provide(scope=Scope.APP)
    def get_kafka_producer(self, settings: KafkaSettings) -> Producer:
        producer = Producer(
            {"bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS}
        )
        return producer


class KafkaProducerServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def get_kafka_producer_service(self, producer: Producer) -> KafkaProducer:
        return KafkaProducer(producer=producer, topic="dlq")


class KafkaConsumerProvider(Provider):
    @provide(scope=Scope.APP)
    def get_kafka_consumer(self, settings: KafkaSettings) -> Generator[Consumer]:
        consumer = Consumer(
            {
                "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
                "group.id": settings.KAFKA_CONSUMER_GROUP,
                "enable.auto.commit": False,
                "auto.offset.reset": "earliest",
            }
        )
        try:
            yield consumer
        finally:
            consumer.close()


class KafkaConsumerServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def get_kafka_consumer_service(self, consumer: Consumer, 
                                   settings: KafkaSettings,
                                   app_settings: AppSettings) -> KafkaConsumer:
        return KafkaConsumer(consumer=consumer,
                             batch_size=app_settings.BATCH_SIZE,
                             topic=settings.KAFKA_TOPIC)
