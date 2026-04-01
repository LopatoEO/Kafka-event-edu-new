import asyncio
from aiokafka.admin import AIOKafkaAdminClient, NewTopic

BROKERS = ["kafka-0:9092", "kafka-1:9092", "kafka-2:9092"]
TOPICS = [
    NewTopic(name="events", num_partitions=3, replication_factor=2),
    NewTopic(name="dlq", num_partitions=3, replication_factor=2),
]

def wait_for_kafka():
    import socket
    import time

    while True:
        try:
            with socket.create_connection(("kafka-0", 9092), timeout=5):
                return
        except OSError:
            time.sleep(5)


async def create_topics(brokers: str):
    wait_for_kafka()
    admin = AIOKafkaAdminClient(bootstrap_servers=brokers.split(","))
    await admin.start()
    try:
        existing = await admin.list_topics()
        for topic in TOPICS:
            if topic.name not in existing:
                print(f"Creating topic {topic.name}...")
                await admin.create_topics([topic])
            else:
                print(f"Topic {topic.name} already exists.")
    finally:
        await admin.close()
    
