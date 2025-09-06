from fastapi import FastAPI
from music_system.database import Base, engine
from music_system.routes.auth import router as auth_router
from music_system.routes.search import router as search_router
# from music_system.routes.event import router as event_router
from music_system.helpers.kafka_helper import kafka_helper
from music_system.schemas.event import UserEvent

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Music System API")
app.include_router(auth_router)
app.include_router(search_router)
# app.include_router(event_router)

@app.get("/")
def root():
    return {"message": "Music System API is running!"}

@app.post("/event")
async def track_event(event: UserEvent):
    event_data = event.model_dump()
    kafka_helper.send_event(event_data)
    return {"status": "Event sent to Kafka"}