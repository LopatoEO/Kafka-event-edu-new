from typing import Generator
from confluent_kafka import Producer, Consumer
from dishka import Provider, provide, Scope
from src.settings import settings
from src.broker.consumer import KafkaConsumer
from src.broker.producer import KafkaProducer



class KafkaProducerProvider(Provider):
    @provide(scope=Scope.APP)
    def get_kafka_producer(self) -> Producer:
        producer = Producer({"bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS})
        return producer

class KafkaProducerServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def get_kafka_producer_service(self, producer: Producer) -> KafkaProducer:
        return KafkaProducer(producer=producer, topic='dlq')

class KafkaConsumerProvider(Provider):
    @provide(scope=Scope.APP)
    def get_kafka_consumer(self) -> Generator[Consumer, None]:
        consumer = Consumer({"bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
                             "group.id": settings.KAFKA_CONSUMER_GROUP,
                             "enable.auto.commit": False,
                             "auto.offset.reset": "earliest"})
        try:
            yield consumer
        finally:
            consumer.close()

class KafkaConsumerServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def get_kafka_consumer_service(self, consumer: Consumer) -> KafkaConsumer:
        return KafkaConsumer(consumer=consumer, topic=settings.KAFKA_TOPIC)