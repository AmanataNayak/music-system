from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from music_system.database import Base

class UserEvent(Base):
    __tablename__ = "user_events"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    song_id = Column(UUID(as_uuid=True), ForeignKey("songs.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(50), nullable=False)
    event_timestamp = Column(TIMESTAMP, server_default=func.now())

