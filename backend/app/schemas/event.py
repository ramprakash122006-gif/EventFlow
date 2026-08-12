from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict
from app.schemas.registration import RegistrationResponse

class EventBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150, description="Event title")
    description: Optional[str] = Field(None, description="Event description")
    location: str = Field(..., min_length=2, max_length=200, description="Event location")
    start_time: datetime = Field(..., description="Event start date and time")
    total_capacity: int = Field(..., gt=0, description="Maximum seating capacity")

    @field_validator("title", "location", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    confirmed_count: int = Field(..., description="Number of confirmed attendees")
    waitlisted_count: int = Field(..., description="Number of waitlisted attendees")
    available_seats: int = Field(..., description="Seats remaining")
    is_full: bool = Field(..., description="True if no confirmed seats left")
    created_at: datetime


class EventDetailResponse(EventResponse):
    registrations: List[RegistrationResponse] = []
