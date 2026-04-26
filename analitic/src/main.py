from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from analitic.src.depencies.clickhouse_provider import ClickHouseProvider, EventServiceProvider
from fastapi import FastAPI
from src.api import v1


app = FastAPI(root_path="/analitic")
app.include_router(v1.router)

container = make_async_container(
    ClickHouseProvider(),
    EventServiceProvider(),
)

setup_dishka(container, app)
