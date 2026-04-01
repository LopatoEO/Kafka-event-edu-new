from aiokafka import AIOKafkaConsumer
import asyncio
import json
import os
from aiochclient import ChClient
from .dispatcher.router import dispatcher
from .repository.event_repository import EventRepository
from .batch_writer.batch_writer import BatchWriter
from .kafka_init import create_topics

async def consume():
    kafka_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka-0:9094,kafka-1:9095,kafka-2:9096")
    ch_host = os.getenv("CLICKHOUSE_HOST", "clickhouse-node1")
    ch_port = os.getenv("CLICKHOUSE_PORT", "8123")
    ch_url = f"http://{ch_host}:{ch_port}/"
    await create_topics(kafka_servers)
    
    ch_client = ChClient(url=ch_url, database='kafka_events')
    
    repo = EventRepository(ch_client)
    
    consumer = AIOKafkaConsumer(
        "events",
        bootstrap_servers=kafka_servers.split(","),
        group_id="my_group",
        enable_auto_commit=False,
        auto_offset_reset="earliest"
    )

    await consumer.start()
    
    batch_writer = BatchWriter(repo, commit_func=lambda: consumer.commit())
    
    dispatcher.batch_writer = batch_writer
    
    try:
        async for msg in consumer:
            event = json.loads(msg.value.decode('utf-8'))    
            await dispatcher.dispatch(event)         
    finally:
        await batch_writer.flush()
        await consumer.stop()
        await ch_client.close()

asyncio.run(consume())