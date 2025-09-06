from fastapi import APIRouter
from music_system.helpers.kafka_helper import kafka_helper
from music_system.schemas.event import UserEvent

router = APIRouter(prefix="/api/play-song", tags=["Event"])

router.post("/")
async def track_event(event: UserEvent):
    event_data = event.model_dump()
    kafka_helper.topic = 'user-events'
    kafka_helper.send_event(event_data)
    return {"status": "Event sent to Kafka"}
