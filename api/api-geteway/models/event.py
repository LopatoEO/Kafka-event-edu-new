from pydantic import BaseModel, Field
from datetime import datetime, timezone



class Event(BaseModel):
    user_id: int 
    event: str
    value: int
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EventsSearchParams(BaseModel):
    user_id: int | None = None
    event: str | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None

class EventResponse(BaseModel):
    user_id: int
    type: str
    value: str
    ts: datetime

class EventsResponseList(BaseModel):
    events: list[EventResponse]
