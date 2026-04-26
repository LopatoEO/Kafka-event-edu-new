import json
import time
from typing import Callable

from src.batch_writer import BatchWriter
from src.broker.consumer import IConsumer
from src.broker.producer import IProducer


class EventDispatcher:
    def __init__(self, field: str) -> None:
        self.field = field
        self._handlers = {}

    def register_depencies(
        self,
        batch_writer: BatchWriter,
        consumer: IConsumer,
        producer: IProducer,
    ) -> None:
        self.batch_writer = batch_writer
        self.consumer = consumer
        self.producer = producer

    def handler(self, value) -> Callable:
        def decorator(func):
            self._handlers[value] = func
            return func

        return decorator

    def _dispatch(self, event) -> None:
        key = event.get(self.field)
        handler = self._handlers.get(key)

        if handler:
            handler(event)
        else:
            self._default(event)

    def _default(self, event) -> None:
        self.producer.send(key=event.get(self.field), value=json.dumps(event))

    def run(self) -> None:
        if not self.batch_writer or not self.consumer:
            raise Exception("Dependencies not registered")
        while True:
            messages = self.consumer.poll()
            if messages is None:
                continue
            for message in messages:
                self._dispatch(message)
            is_commited = self.batch_writer.commit()
            if is_commited:
                self.consumer.commit()
            time.sleep(1)
