from pydantic_settings import BaseSettings


class ClickHouseSettings(BaseSettings):
    CLICKHOUSE_HOST: str = "127.0.0.1"
    CLICKHOUSE_PORT: int = 8123
    CLICKHOUSE_USER: str = "default"
    CLICKHOUSE_PASSWORD: str = ""
    CLICKHOUSE_DATABASE: str = "kafka_events"
    BATCH_SIZE: int = 10

    @property
    def url(self):
        return 