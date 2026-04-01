from datetime import datetime
from pydantic import BaseModel

class EventsSearchParams(BaseModel):
    user_id: int | None = None
    event: str | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None

class Event(BaseModel):
    user_id: int
    type: str
    value: str
    ts: datetime

class EventsResponse(BaseModel):
    events: list[Event]
