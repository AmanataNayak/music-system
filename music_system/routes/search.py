from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from music_system.database import get_db
from music_system.schemas.search import SearchResult, TrackMetadata
from music_system.services.search_service import search_full_text, get_track

router = APIRouter(prefix="/api/search", tags=["Search"])

@router.get("/", response_model=list[SearchResult])
def search(query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return search_full_text(db, query)

@router.get("/tracks/{track_id}", response_model=TrackMetadata)
def search_track(track_id: str, db: Session = Depends(get_db)):
    track = get_track(db, track_id)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return track