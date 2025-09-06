from kafka import KafkaConsumer
import json
from datetime import datetime
from music_system.database import SessionLocal, engine, Base
from sqlalchemy import text
import uuid
from uuid import UUID
import datetime as dt

Base.metadata.create_all(bind=engine)

consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Worker listening to Kafka events...")

for message in consumer:
    event = message.value
    print(f"Processing event: {event}")

    db = SessionLocal()
    try:
        # db_event = UserEvent(
        #     id=uuid.uuid4(),
        #     user_id=uuid.UUID(event.get('user_id')),
        #     song_id=uuid.UUID(event.get('song_id')),
        #     event_type=event.get('event_type'),
        #     event_timestamp=event.get('timestamp', datetime.utcnow())
        # )
        query = text("""INSERT INTO user_events VALUES(:id, :user_id, :song_id, :event_type, :event_timestamp)""")
        db.execute(query, {'id': uuid.uuid4(), "user_id": UUID(event['user_id']), 
                           "song_id": UUID(event["song_id"]), "event_type": event['event_type'], 
                           "event_timestamp": event.get("event_timestamp", datetime.now(dt.UTC))})
        print("Done")
        db.commit()
    except Exception as e:
        print(f"Failed to insert event: {e}")
        db.rollback()
    finally:
        db.close()
