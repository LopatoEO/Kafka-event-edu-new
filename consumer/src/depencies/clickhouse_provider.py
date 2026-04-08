import clickhouse_connect
from clickhouse_connect.driver import Client
from dishka import Provider, provide, Scope
from src.settings import settings
from src.repository.event_repository import EventRepository
from src.batch_writer.batch_writer import BatchWriter

class ClickHouseClientProvider(Provider):
    @provide(scope=Scope.APP)
    def get_clickhouse_client(self) -> Client:
        client = clickhouse_connect.get_client(
                        host=settings.CLICKHOUSE_HOST,  
                        port=settings.CLICKHOUSE_PORT, 
                        username=settings.CLICKHOUSE_USER, 
                        password=settings.CLICKHOUSE_PASSWORD, 
                        database=settings.CLICKHOUSE_DATABASE)
        return client
    
class RepositoryProvider(Provider):
    @provide(scope=Scope.APP)
    def get_repository(self, clickhouse_client: Client) -> EventRepository:
        return EventRepository(clickhouse_client)
    
class BatchWriterProvider(Provider):
    @provide(scope=Scope.APP)
    def get_batch_writer(self, repository: EventRepository) -> BatchWriter:
        return BatchWriter(repository)