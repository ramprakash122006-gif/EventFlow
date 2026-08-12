from fastapi import Request, status
from fastapi.responses import JSONResponse

class DomainException(Exception):
    def __init__(self, message: str, error_code: str = "BAD_REQUEST", status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)

class DuplicateRegistrationException(DomainException):
    def __init__(self, email: str):
        super().__init__(
            message=f"Email '{email}' is already registered for this event.",
            error_code="DUPLICATE_REGISTRATION",
            status_code=status.HTTP_409_CONFLICT
        )

class CapacityExceededException(DomainException):
    def __init__(self, event_title: str):
        super().__init__(
            message=f"Event '{event_title}' has reached its maximum capacity.",
            error_code="CAPACITY_EXCEEDED",
            status_code=status.HTTP_409_CONFLICT
        )

class EventNotFoundException(DomainException):
    def __init__(self, event_id: int):
        super().__init__(
            message=f"Event with ID {event_id} was not found.",
            error_code="EVENT_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )

class RegistrationNotFoundException(DomainException):
    def __init__(self, registration_id: int):
        super().__init__(
            message=f"Registration with ID {registration_id} was not found.",
            error_code="REGISTRATION_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )

class PastEventException(DomainException):
    def __init__(self, event_title: str):
        super().__init__(
            message=f"Cannot register for past event '{event_title}'.",
            error_code="PAST_EVENT_REGISTRATION",
            status_code=status.HTTP_400_BAD_REQUEST
        )

class AlreadyCancelledException(DomainException):
    def __init__(self):
        super().__init__(
            message="This registration is already cancelled.",
            error_code="ALREADY_CANCELLED",
            status_code=status.HTTP_400_BAD_REQUEST
        )

async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "error_code": exc.error_code
        }
    )
