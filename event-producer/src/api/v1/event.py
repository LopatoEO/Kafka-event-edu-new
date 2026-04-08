from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dishka.integrations.fastapi import inject
from dishka import FromDishka
from src.models.event import EventDTO
from src.service.event_service import EventService

router = APIRouter(tags=["events"])

@router.post("/")
@inject
async def create_message(message: EventDTO, 
                         producer: FromDishka[EventService]) -> JSONResponse:
    await producer.send_event('events',message)
    return JSONResponse(content=jsonable_encoder({"received": message}),
                        status_code=201)