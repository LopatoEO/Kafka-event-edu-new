import json
import os

from fastapi import APIRouter, Depends
from aiokafka import AIOKafkaProducer
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from aiohttp import ClientSession

from ...depencies.producer import get_producer
from ...depencies.http_session import get_session
from ...models.event import *


router = APIRouter(tags=["events"])

# POST-ручка
@router.post("/")
async def create_message(message: Event, 
                         producer: AIOKafkaProducer = Depends(get_producer)):
    await producer.send_and_wait(
        'events',
        message.json().encode('utf-8'),
        key=f'user_id:{message.user_id}'.encode('utf-8')
    )
    return JSONResponse(content=jsonable_encoder({"received": message}),
                        status_code=201)

@router.get("/")
async def create_message(message: EventsSearchParams = Depends(),
                         session: ClientSession = Depends(get_session)) -> EventsResponseList:
    params = {
        "user_id": message.user_id if message.user_id is not None else None,
        "event": message.event if message.event is not None else None,
        "date_from": message.date_from.isoformat() ,
        "date_to": message.date_to.isoformat()
    }
    params = {k: v for k, v in params.items() if v is not None}
    host = os.getenv('ANALITICS_SERVICE_HOST', 'analitic')
    port = os.getenv('ANALITICS_SERVICE_PORT', '8001')
    url = f"http://{host}:{port}/v1/events"
    async with session.get(
        url,    
        params=params
    ) as resp:
        raw_events = await resp.json()
    print(raw_events)
    if raw_events.get('events') is None:
        raise HTTPException(status_code=404, detail="Events not found")
    return EventsResponseList(events=[EventResponse (**event) for event in raw_events['events']])