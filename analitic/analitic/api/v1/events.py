from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from ...depencies.depencies import get_ch
from ...schemas.events import EventsSearchParams, EventsResponse, Event
from ...service.events_service import EventsService


router = APIRouter(tags=["events"])

@router.get("/")
async def create_message(message: EventsSearchParams = Depends(),
                         client = Depends(get_ch)):
    service = EventsService(client)
    events = await service.get_events(message.user_id, message.event, message.date_from, message.date_to)
    if not events:
        raise HTTPException(status_code=404, detail="Events not found")
    return EventsResponse(events=[Event(**event) for event in events])