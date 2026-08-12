from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.registration import RegistrationResponse
from app.services.registration_service import RegistrationService

router = APIRouter(prefix="/registrations", tags=["Registrations"])

@router.post("/{registration_id}/cancel", response_model=RegistrationResponse)
def cancel_registration(registration_id: int, db: Session = Depends(get_db)):
    """Cancel a registration and automatically promote the next waitlisted user if available."""
    return RegistrationService.cancel_registration(db, registration_id)
