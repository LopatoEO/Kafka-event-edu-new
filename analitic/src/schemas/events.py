from datetime import datetime
from pydantic import BaseModel

class EventsSearchParamsDTO(BaseModel):
    user_id: int | None = None
    event: str | None = None
    date_from: datetime
    date_to: datetime

class EventDTO(BaseModel):
    user_id: int
    type: str
    value: str
    ts: datetime

class EventsResponseDTO(BaseModel):
    events: list[EventDTO]
