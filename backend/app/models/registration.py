import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from app.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class RegistrationStatus(str, enum.Enum):
    CONFIRMED = "CONFIRMED"
    WAITLISTED = "WAITLISTED"
    CANCELLED = "CANCELLED"

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    status = Column(SQLEnum(RegistrationStatus), nullable=False, default=RegistrationStatus.CONFIRMED)
    registered_at = Column(DateTime(timezone=True), default=utc_now)

    event = relationship("Event", back_populates="registrations")

    __table_args__ = (
        Index("idx_event_email", "event_id", "email"),
    )
