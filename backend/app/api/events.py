from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.event import EventCreate, EventResponse, EventDetailResponse
from app.schemas.registration import RegistrationCreate, RegistrationResponse
from app.services.event_service import EventService
from app.services.registration_service import RegistrationService

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("", response_model=List[EventResponse])
def list_events(db: Session = Depends(get_db)):
    """List all events with capacity and remaining seat statistics."""
    return EventService.list_events(db)

@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event_in: EventCreate, db: Session = Depends(get_db)):
    """Create a new event."""
    return EventService.create_event(db, event_in)

@router.get("/{event_id}", response_model=EventDetailResponse)
def get_event_detail(event_id: int, db: Session = Depends(get_db)):
    """Get detailed information about an event including attendees."""
    return EventService.get_event_detail(db, event_id)

@router.post("/{event_id}/register", response_model=RegistrationResponse)
def register_for_event(event_id: int, reg_in: RegistrationCreate, db: Session = Depends(get_db)):
    """Register attendee for an event (enforces seat capacity and prevents duplicate emails)."""
    registration = RegistrationService.register_user(db, event_id, reg_in)
    return registration

@router.get("/{event_id}/registrations", response_model=List[RegistrationResponse])
def get_event_registrations(event_id: int, db: Session = Depends(get_db)):
    """List all registrations for a specific event."""
    return RegistrationService.get_event_registrations(db, event_id)
