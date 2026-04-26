from typing import AsyncIterable
from dishka import Provider, provide, Scope
from aiochclient import ChClient
from aiohttp import ClientSession
from src.services.events_service import EventsService
from src.repositories.events_repository_clickhouse import EventRepository
from analitic.src.settings.clickhouse_settings import ClickHouseSettings
from analitic.src.settings.settings import settings


class ClickHouseSettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_clickhouse_settings(self) -> ClickHouseSettings:
        return settings.CLICKHOUSE_SETTINGS

class ClickHouseProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_clickhouse(self, settings: ClickHouseSettings) -> AsyncIterable[ChClient]:
        session = ClientSession()
        try:
            client = ChClient(
                session=session,
                url=settings.url,
                user=settings.CLICKHOUSE_USERNAME,
                password=settings.CLICKHOUSE_PASSWORD,
                database=settings.CLICKHOUSE_DATABASE,
            )
            yield client
        finally:
            await session.close()

class EventRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_repository(self, client: ChClient) -> EventRepository:
        return EventRepository(client)

class EventServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_service(self, repository: EventRepository) -> EventsService:
        return EventsService(repository)