from pydantic_settings import BaseSettings

class ClickHouseSettings(BaseSettings):
    CLICKHOUSE_HOST: str = "FastAPIApp"
    CLICKHOUSE_PORT: str = "8123"
    CLICKHOUSE_USERNAME: str = "default"
    CLICKHOUSE_PASSWORD: str = ""
    CLICKHOUSE_DATABASE: str = "kafka_events"


    @property
    def url(self) -> str:
        return f"http://{self.CLICKHOUSE_HOST}:{self.CLICKHOUSE_PORT}"      