from pydantic import BaseModel
from enum import Enum

class Type(str, Enum):
    SONG="song"
    ALBUM="album"
    artist="artist"


class SearchResult(BaseModel):
    type: Type
    id: str
    title: str

