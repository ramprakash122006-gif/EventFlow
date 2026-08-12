from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from app.models.registration import RegistrationStatus

class RegistrationCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100, description="Full name of attendee")
    email: EmailStr = Field(..., description="Attendee email address")

    @field_validator("full_name", mode="before")
    @classmethod
    def strip_full_name(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v

class RegistrationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    full_name: str
    email: str
    status: RegistrationStatus
    registered_at: datetime

