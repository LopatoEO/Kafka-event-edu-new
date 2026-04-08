from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka-0:9092,kafka-1:9092,kafka-2:9092"

settings = AppSettings()