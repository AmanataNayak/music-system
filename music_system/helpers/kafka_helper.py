from kafka import KafkaProducer
import json
from datetime import datetime
import datetime as dt
from music_system.utils.util_classes import Singleton
from uuid import UUID

class KafkaHelper(metaclass=Singleton):
    def __init__(self, server: str="localhost:9092", topic: str = "user-events"):
        self.producer = KafkaProducer(
            bootstrap_servers=server,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            api_version=(2,8)
        )
        self.topic = topic

    @staticmethod
    def uuid_str_converter(event_data: dict):
        for key, value in event_data.items():
            if isinstance(value, UUID):
                event_data[key] = str(value)
        return event_data
    
    def send_event(self, event_data: dict):
        """Send an event to kafka"""
        if "timestamp" not in event_data or event_data["timestamp"] is None:
            event_data["timestamp"] = datetime.now(dt.UTC).isoformat()
        event_data = KafkaHelper.uuid_str_converter(event_data)
        self.producer.send(self.topic, value=event_data)
        self.producer.flush()

kafka_helper = KafkaHelper()
