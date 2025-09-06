from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UserEvent(BaseModel):
    user_id: UUID
    song_id: UUID
    event_type: str
    timestamp: datetime = None
