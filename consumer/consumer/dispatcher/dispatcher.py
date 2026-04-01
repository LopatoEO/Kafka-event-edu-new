import json
import os
from aiokafka import AIOKafkaProducer

class EventDispatcher:
    def __init__(self, field: str, batch_writer=None):
        self.kafka_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS",
                                  "kafka-0:9094,kafka-1:9095,kafka-2:9096")
        self.field = field
        self.batch_writer = batch_writer
        self._handlers = {}

    def handler(self, value):
        def decorator(func):
            self._handlers[value] = func
            return func
        return decorator

    async def dispatch(self, event):
        key = event.get(self.field)
        handler = self._handlers.get(key)

        if handler:
            await handler(event, self.batch_writer)
        else:
            await self.default(event)

    async def default(self, event):
        producer =  AIOKafkaProducer(bootstrap_servers=self.kafka_servers.split(","))
        await producer.start()
        try:    
            await producer.send_and_wait("dlq", json.dumps(event).encode("utf-8"))
        finally:
            await producer.stop()