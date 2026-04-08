import json
import os
import time
from src.batch_writer import BatchWriter
from src.broker.consumer import ConsumerABC
from src.broker.producer import ProducerABC

class EventDispatcher:
    def __init__(self, field: str):
        self.field = field
        self._handlers = {}

    def register_depencies(self,
                           batch_writer: BatchWriter,
                           consumer: ConsumerABC,
                           producer: ProducerABC):
        self.batch_writer = batch_writer
        self.consumer = consumer
        self.producer = producer

    def handler(self, value):
        def decorator(func):
            self._handlers[value] = func
            return func
        return decorator

    def _dispatch(self, event):
        key = event.get(self.field)
        handler = self._handlers.get(key)

        if handler:
            handler(event)
        else:
            self._default(event)

    def _default(self, event):
        self.producer.send(key=event.get(self.field), value=json.dumps(event))

    def run(self):
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
            