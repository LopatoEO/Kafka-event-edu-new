from pydantic_settings import BaseSettings
from src.settings.kafka import KafkaSettings


class AppSettings(BaseSettings):
    KAFKA_SETTINGS: KafkaSettings = KafkaSettings()


app_settings = AppSettings()
