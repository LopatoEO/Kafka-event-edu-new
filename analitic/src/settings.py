from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    CLICKHOUSE_HOST: str = "FastAPIApp"
    CLICKHOUSE_PORT: str = "8123"
    CLICKHOUSE_USERNAME: str = "default"
    CLICKHOUSE_PASSWORD: str = ""
    CLICKHOUSE_DATABASE: str = "kafka_events"

settings = AppSettings()