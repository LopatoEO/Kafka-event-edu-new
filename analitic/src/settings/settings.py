from pydantic_settings import BaseSettings

from src.settings.clickhouse_settings import ClickHouseSettings

class AppSettings(BaseSettings):
    CLICKHOUSE_SETTINGS: ClickHouseSettings = ClickHouseSettings()

settings = AppSettings()