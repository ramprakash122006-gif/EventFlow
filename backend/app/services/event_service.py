from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.event import Event
from app.models.registration import Registration, RegistrationStatus
from app.schemas.event import EventCreate, EventResponse, EventDetailResponse
from app.exceptions import EventNotFoundException

class EventService:
    @staticmethod
    def get_event_by_id(db: Session, event_id: int) -> Event:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise EventNotFoundException(event_id)
        return event

    @staticmethod
    def calculate_seat_stats(db: Session, event: Event) -> dict:
        confirmed_count = db.query(func.count(Registration.id)).filter(
            Registration.event_id == event.id,
            Registration.status == RegistrationStatus.CONFIRMED
        ).scalar() or 0

        waitlisted_count = db.query(func.count(Registration.id)).filter(
            Registration.event_id == event.id,
            Registration.status == RegistrationStatus.WAITLISTED
        ).scalar() or 0

        available_seats = max(0, event.total_capacity - confirmed_count)
        is_full = available_seats == 0

        return {
            "confirmed_count": confirmed_count,
            "waitlisted_count": waitlisted_count,
            "available_seats": available_seats,
            "is_full": is_full
        }

    @classmethod
    def create_event(cls, db: Session, event_in: EventCreate) -> EventResponse:
        event = Event(
            title=event_in.title,
            description=event_in.description,
            location=event_in.location,
            start_time=event_in.start_time,
            total_capacity=event_in.total_capacity
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        stats = cls.calculate_seat_stats(db, event)
        return EventResponse(
            id=event.id,
            title=event.title,
            description=event.description,
            location=event.location,
            start_time=event.start_time,
            total_capacity=event.total_capacity,
            created_at=event.created_at,
            **stats
        )

    @classmethod
    def list_events(cls, db: Session) -> List[EventResponse]:
        events = db.query(Event).order_by(Event.start_time.asc()).all()
        results = []
        for event in events:
            stats = cls.calculate_seat_stats(db, event)
            results.append(
                EventResponse(
                    id=event.id,
                    title=event.title,
                    description=event.description,
                    location=event.location,
                    start_time=event.start_time,
                    total_capacity=event.total_capacity,
                    created_at=event.created_at,
                    **stats
                )
            )
        return results

    @classmethod
    def get_event_detail(cls, db: Session, event_id: int) -> EventDetailResponse:
        event = cls.get_event_by_id(db, event_id)
        stats = cls.calculate_seat_stats(db, event)
        
        registrations = db.query(Registration).filter(
            Registration.event_id == event.id
        ).order_by(Registration.registered_at.asc()).all()

        return EventDetailResponse(
            id=event.id,
            title=event.title,
            description=event.description,
            location=event.location,
            start_time=event.start_time,
            total_capacity=event.total_capacity,
            created_at=event.created_at,
            registrations=registrations,
            **stats
        )
