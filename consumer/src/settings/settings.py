from pydantic_settings import BaseSettings

from src.settings.clickhouse import ClickHouseSettings
from src.settings.kafka import KafkaSettings


class AppSettings(BaseSettings):
    KAFKA_SETTINGS: KafkaSettings = KafkaSettings()
    CLICKHOUSE_SETTINGS: ClickHouseSettings = ClickHouseSettings()
    BATCH_SIZE: int = 10


app_settings = AppSettings()
