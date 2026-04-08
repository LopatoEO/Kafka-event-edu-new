from confluent_kafka import Consumer, KafkaException, Message
import time
import json
from abc import ABC, abstractmethod
from src.settings import settings

class ConsumerABC(ABC):
    @abstractmethod
    def poll(self) -> list[dict]:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

class KafkaConsumer(ConsumerABC):
    def __init__(self,
                consumer: Consumer,
                topic: str, poll_timeout=1.0):
        self.topic = topic
        self.poll_timeout = poll_timeout
        self.consumer = consumer
        self.consumer.subscribe([self.topic])
        self.num_messages = settings.BATCH_SIZE
        self.last_message = None

    def poll(self) -> list[dict]:
        try:
            messages = self.consumer.consume(self.num_messages, timeout=self.poll_timeout)
            valid_messages = [m for m in messages if m is not None and not m.error() and m.value() is not None]
            self.last_message = valid_messages[-1] if valid_messages else None
            return [json.loads(m.value().decode('utf-8')) for m in valid_messages]
        except KafkaException:
            time.sleep(5)
            return []

    def commit(self) -> None:
        if self.last_message is not None:
            self.consumer.commit(message=self.last_message)

    def close(self) -> None:
        self.consumer.close()