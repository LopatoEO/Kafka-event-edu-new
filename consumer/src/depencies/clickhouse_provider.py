import clickhouse_connect
from clickhouse_connect.driver import Client
from consumer.src.repository.event_repository_clickhouse import EventRepository
from dishka import Provider, Scope, provide

from src.batch_writer.batch_writer import BatchWriter
from src.settings.clickhouse import ClickHouseSettings
from src.settings.settings import AppSettings, app_settings


class ClickHouseSettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_clickhouse_settings(self) -> ClickHouseSettings:
        return app_settings.CLICKHOUSE_SETTINGS

class BatchSizeProvider(Provider):
    @provide(scope=Scope.APP)
    def get_app_settings(self) -> int:
        return app_settings.BATCH_SIZE

class ClickHouseClientProvider(Provider):
    @provide(scope=Scope.APP)
    def get_clickhouse_client(self, settings: ClickHouseSettings) -> Client:
        client = clickhouse_connect.get_client(
            host=settings.CLICKHOUSE_HOST,
            port=settings.CLICKHOUSE_PORT,
            username=settings.CLICKHOUSE_USER,
            password=settings.CLICKHOUSE_PASSWORD,
            database=settings.CLICKHOUSE_DATABASE,
        )
        return client


class RepositoryProvider(Provider):
    @provide(scope=Scope.APP)
    def get_repository(self, clickhouse_client: Client) -> EventRepository:
        return EventRepository(clickhouse_client)


class BatchWriterProvider(Provider):
    @provide(scope=Scope.APP)
    def get_batch_writer(self, repository: EventRepository,
                         app_settings: AppSettings) -> BatchWriter:
        return BatchWriter(repository, app_settings.BATCH_SIZE)
