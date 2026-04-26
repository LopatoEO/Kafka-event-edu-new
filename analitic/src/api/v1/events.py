from fastapi import APIRouter, Query, HTTPException
from typing import Annotated
from dishka.integrations.fastapi import FromDishka, inject
from src.schemas.events import EventsSearchParamsDTO, EventListResponseDTO
from src.services.events_service import EventsService

event_router = APIRouter(tags=["events"])

@event_router.get("/")
@inject
async def get_events(
    message: Annotated[EventsSearchParamsDTO, Query()],
    service: FromDishka[EventsService],
) -> EventListResponseDTO:
    events = await service.get_events(search_params=message)
    if not events:
        raise HTTPException(status_code=404, detail="Events not found")
    return events