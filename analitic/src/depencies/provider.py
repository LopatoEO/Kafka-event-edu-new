from typing import AsyncIterable
from dishka import Provider, provide, Scope
from aiochclient import ChClient
from aiohttp import ClientSession
from src.service.events_service import EventsService
from src.settings import settings


class ClickHouseProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_clickhouse(self) -> AsyncIterable[ChClient]:
        session = ClientSession()
        try:
            url = f"http://{settings.CLICKHOUSE_HOST}:{settings.CLICKHOUSE_PORT}"
            client = ChClient(
                session=session,
                url=url,
                user=settings.CLICKHOUSE_USERNAME,
                password=settings.CLICKHOUSE_PASSWORD,
                database=settings.CLICKHOUSE_DATABASE,
            )
            yield client
        finally:
            await session.close()

class EventServiceProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def get_service(self, client: ChClient) -> EventsService:
        return EventsService(client)