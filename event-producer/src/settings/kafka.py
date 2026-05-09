from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = (
        "localhost:9094, localhost:9095, localhost:9096"
    )
    KAFKA_CONSUMER_GROUP: str = "event_consumers"
    KAFKA_TOPIC: str = "events"
