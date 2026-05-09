from pydantic import BaseModel, Field
from datetime import datetime, timezone


class EventDTO(BaseModel):
    user_id: int 
    event: str
    value: int
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
