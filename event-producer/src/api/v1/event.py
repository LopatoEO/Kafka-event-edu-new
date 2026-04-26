from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dishka.integrations.fastapi import inject
from dishka import FromDishka
from src.models.event import EventDTO
from src.services.event_service import EventService

event_router = APIRouter(tags=["events"])

@event_router.post("/")
@inject
async def create_message(message: EventDTO, 
                         service: FromDishka[EventService]) -> JSONResponse:
    await service.send_event(message)
    return JSONResponse(content=jsonable_encoder({"received": message}),
                        status_code=201)