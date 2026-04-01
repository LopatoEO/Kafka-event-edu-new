from aiokafka import AIOKafkaProducer
from typing import AsyncGenerator
import os


async def get_producer() -> AsyncGenerator[AIOKafkaProducer, None]:
    kafka_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka-0:9092,kafka-1:9092,kafka-2:9092")
    producer = AIOKafkaProducer(bootstrap_servers=kafka_servers.split(","))
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()