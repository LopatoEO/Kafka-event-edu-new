import json
import time
from abc import ABC, abstractmethod

from confluent_kafka import Consumer, KafkaException


class IConsumer(ABC):
    @abstractmethod
    def poll(self) -> list[dict]:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class KafkaConsumer(IConsumer):
    def __init__(
       self, consumer: Consumer,
       batch_size: int,
       topic: str, poll_timeout=1.0) -> None:
        self.topic = topic
        self.poll_timeout = poll_timeout
        self._consumer = consumer
        self._consumer.subscribe([self.topic])
        self.num_messages = batch_size
        self.last_message = None

    def poll(self) -> list[dict]:
        try:
            messages = self._consumer.consume(
                self.num_messages, timeout=self.poll_timeout
            )
            valid_messages = [
                m
                for m in messages
                if m is not None and not m.error() and m.value() is not None
            ]
            self.last_message = valid_messages[-1] if valid_messages else None
            return [
                json.loads(m.value().decode("utf-8")) for m in valid_messages
            ]
        except KafkaException:
            time.sleep(5)
            return []

    def commit(self) -> None:
        if self.last_message is not None:
            self._consumer.commit(message=self.last_message)

    def close(self) -> None:
        self._consumer.close()
