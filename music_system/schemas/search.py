from pydantic import BaseModel
from enum import Enum
from typing import Optional
from uuid import UUID
import datetime

class Type(str, Enum):
    SONG="song"
    ALBUM="album"
    artist="artist"


class SearchResult(BaseModel):
    type: Type
    id: str
    title: str

class TrackMetadata(BaseModel):
    id: UUID
    title: str
    duration: int
    language: Optional[str]
    release_date: Optional[datetime.date]
    album_id: Optional[UUID]
    album_title: Optional[str]
    artist_id: UUID
    artist_name: str
