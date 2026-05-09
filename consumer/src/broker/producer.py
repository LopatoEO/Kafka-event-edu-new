from abc import ABC, abstractmethod

from confluent_kafka import Producer


class IProducer(ABC):
    @abstractmethod
    def send(self, key, value) -> None:
        pass


class KafkaProducer(IProducer):
    def __init__(self, producer: Producer, topic: str) -> None:
        self._producer = producer
        self.topic = topic

    def send(self, key, value) -> None:
        self._producer.produce(topic=self.topic, key=key, value=value)
        self._producer.flush()
