from fastapi import APIRouter, Query, HTTPException
from typing import Annotated
from dishka.integrations.fastapi import FromDishka, inject
from src.schemas.events import EventsSearchParamsDTO, EventsResponseDTO
from src.service.events_service import EventsService

router = APIRouter(tags=["events"])

@router.get("/")
@inject
async def get_events(
    message: Annotated[EventsSearchParamsDTO, Query()],
    service: FromDishka[EventsService],
) -> EventsResponseDTO:
    events = await service.get_events(
        user_id=message.user_id,
        event_type=message.event,
        event_time_from=message.date_from,
        event_time_to=message.date_to
    )
    if not events:
        raise HTTPException(status_code=404, detail="Events not found")
    return events