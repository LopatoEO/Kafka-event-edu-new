from fastapi import FastAPI
from src.api import v1
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka 
from src.depencies.producer import KafkaProvider, EventServiceProvider 

app = FastAPI(root_path='/event-producer')
app.include_router(v1.router)

container = make_async_container(KafkaProvider(),
                                 EventServiceProvider())

setup_dishka(container, app)


