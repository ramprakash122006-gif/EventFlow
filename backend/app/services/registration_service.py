import logging
from datetime import datetime, timezone
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.event import Event
from app.models.registration import Registration, RegistrationStatus
from app.schemas.registration import RegistrationCreate, RegistrationResponse
from app.services.event_service import EventService
from app.exceptions import (
    DuplicateRegistrationException,
    PastEventException,
    RegistrationNotFoundException,
    AlreadyCancelledException
)

logger = logging.getLogger("uvicorn")

class RegistrationService:
    @classmethod
    def register_user(cls, db: Session, event_id: int, reg_in: RegistrationCreate) -> RegistrationResponse:
        # 1. Fetch event (throws EventNotFoundException if not found)
        event = EventService.get_event_by_id(db, event_id)

        # 2. Check past event rule
        now_utc = datetime.now(timezone.utc)
        event_start = event.start_time
        if event_start.tzinfo is None:
            event_start = event_start.replace(tzinfo=timezone.utc)

        if event_start < now_utc:
            logger.warning(f"Registration rejected: Event '{event.title}' is in the past.")
            raise PastEventException(event.title)

        # 3. Check duplicate active registration (case-insensitive email)
        normalized_email = reg_in.email.strip().lower()
        existing_reg = db.query(Registration).filter(
            Registration.event_id == event_id,
            func.lower(Registration.email) == normalized_email,
            Registration.status != RegistrationStatus.CANCELLED
        ).first()

        if existing_reg:
            logger.warning(f"Registration rejected: Email '{normalized_email}' already registered for Event ID {event_id}.")
            raise DuplicateRegistrationException(normalized_email)

        # 4. Enforce capacity check
        stats = EventService.calculate_seat_stats(db, event)
        if stats["confirmed_count"] < event.total_capacity:
            target_status = RegistrationStatus.CONFIRMED
        else:
            target_status = RegistrationStatus.WAITLISTED

        # 5. Create registration within transaction
        registration = Registration(
            event_id=event_id,
            full_name=reg_in.full_name,
            email=normalized_email,
            status=target_status
        )
        db.add(registration)
        db.commit()
        db.refresh(registration)

        logger.info(f"Registered user '{registration.full_name}' ({registration.email}) for Event '{event.title}' -> Status: {registration.status.value}")

        return RegistrationResponse.model_validate(registration)


    @classmethod
    def cancel_registration(cls, db: Session, registration_id: int) -> RegistrationResponse:
        registration = db.query(Registration).filter(Registration.id == registration_id).first()
        if not registration:
            raise RegistrationNotFoundException(registration_id)

        if registration.status == RegistrationStatus.CANCELLED:
            raise AlreadyCancelledException()

        was_confirmed = (registration.status == RegistrationStatus.CONFIRMED)
        registration.status = RegistrationStatus.CANCELLED
        db.commit()
        logger.info(f"Cancelled registration ID {registration_id} ({registration.email})")

        # If a CONFIRMED registration was cancelled, promote earliest WAITLISTED user
        if was_confirmed:
            next_in_line = db.query(Registration).filter(
                Registration.event_id == registration.event_id,
                Registration.status == RegistrationStatus.WAITLISTED
            ).order_by(Registration.registered_at.asc()).first()

            if next_in_line:
                next_in_line.status = RegistrationStatus.CONFIRMED
                db.commit()
                logger.info(f"Auto-promoted waitlisted user '{next_in_line.full_name}' ({next_in_line.email}) to CONFIRMED for Event ID {registration.event_id}")


        db.refresh(registration)
        return RegistrationResponse.model_validate(registration)

    @classmethod
    def get_event_registrations(cls, db: Session, event_id: int) -> List[RegistrationResponse]:
        EventService.get_event_by_id(db, event_id) # Validates event existence
        regs = db.query(Registration).filter(
            Registration.event_id == event_id
        ).order_by(Registration.registered_at.asc()).all()

        return [RegistrationResponse.model_validate(r) for r in regs]
