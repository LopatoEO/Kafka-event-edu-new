from fastapi import FastAPI
from .api import v1
import uvicorn
from aiohttp import ClientSession
from aiochclient import ChClient
import os


app = FastAPI()
app.include_router(v1.router)

@app.on_event("startup")
async def startup():
    session = ClientSession()
    ch_host = os.getenv("CLICKHOUSE_HOST", "clickhouse-node1")
    ch_port = os.getenv("CLICKHOUSE_PORT", "8123")
    clickhouse_url = f"http://{ch_host}:{ch_port}"
    app.state.ch = ChClient(session, url=clickhouse_url, database='kafka_events')

@app.on_event("shutdown")
async def shutdown():
    await app.state.ch._session.close()


if (__name__ == '__main__'):
    uvicorn.run(app, port=8001)

