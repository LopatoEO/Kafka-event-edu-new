from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic
import time
import socket
from src.settings import settings

BROKERS = settings.KAFKA_BOOTSTRAP_SERVERS
FIRST_BROKER = BROKERS.split(",")[0].strip().split(":")

TOPICS = [
    NewTopic(topic="events", num_partitions=3, replication_factor=2),
    NewTopic(topic="dlq", num_partitions=3, replication_factor=2),
]

def wait_for_kafka():
    while True:
        try:
            with socket.create_connection((FIRST_BROKER[0], int(FIRST_BROKER[1])), timeout=5):
                return
        except OSError:
            time.sleep(5)


def create_topics():
    wait_for_kafka()
    admin = AdminClient({"bootstrap.servers": BROKERS})

    existing = admin.list_topics(timeout=10).topics.keys()

    new_topics = [t for t in TOPICS if t.topic not in existing]
    if not new_topics:
        return

    fs = admin.create_topics(new_topics)

    for topic, f in fs.items():
        try:
            f.result()
        except Exception:
            pass


if __name__ == "__main__":
    create_topics()