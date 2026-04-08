from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9094, localhost:9095, localhost:9096"
    KAFKA_CONSUMER_GROUP: str = 'event_consumers'
    KAFKA_TOPIC: str = 'events'
    CLICKHOUSE_HOST: str = "127.0.0.1"
    CLICKHOUSE_PORT: int = 8123
    CLICKHOUSE_USER: str = "default"
    CLICKHOUSE_PASSWORD: str = ""
    CLICKHOUSE_DATABASE: str = "kafka_events"
    BATCH_SIZE: int = 10

settings = AppSettings()