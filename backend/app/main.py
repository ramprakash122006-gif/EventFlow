from datetime import datetime, timedelta, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base, SessionLocal
from app.exceptions import DomainException, domain_exception_handler
from app.api.events import router as events_router
from app.api.registrations import router as registrations_router
from app.models.event import Event

def seed_sample_events():
    db = SessionLocal()
    try:
        if db.query(Event).count() == 0:
            now = datetime.now(timezone.utc)
            sample_events = [
                Event(
                    title="Tech Innovation Summit 2026",
                    description="Join industry leaders to explore the future of AI, Cloud Native, and Event-Driven Architecture.",
                    location="Auditorium A, Tech Hub",
                    start_time=now + timedelta(days=5),
                    total_capacity=3
                ),
                Event(
                    title="React & FastAPI Masterclass",
                    description="Hands-on workshop covering high-performance REST APIs with FastAPI and responsive UI with React.",
                    location="Workshop Room 102",
                    start_time=now + timedelta(days=12),
                    total_capacity=5
                ),
                Event(
                    title="Legacy Systems & Migration (Past Event)",
                    description="Retrospective discussion on migrating monoliths to decoupled microservices.",
                    location="Conference Hall C",
                    start_time=now - timedelta(days=2),
                    total_capacity=10
                )
            ]
            db.add_all(sample_events)
            db.commit()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables
    Base.metadata.create_all(bind=engine)
    # Seed initial demo data (skip during unit test runs)
    if settings.ENVIRONMENT != "testing":
        seed_sample_events()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Event Registration & Capacity Management System API",
    lifespan=lifespan
)

from fastapi.exceptions import RequestValidationError
from fastapi import Request, status
from fastapi.responses import JSONResponse

# Exception handlers
app.add_exception_handler(DomainException, domain_exception_handler)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = err.get("loc", [])[-1]
        if field == "email":
            errors.append("Please enter a valid email address (e.g. user@example.com).")
        elif field == "full_name":
            errors.append("Full name must be between 2 and 100 characters.")
        else:
            errors.append(f"Invalid {field}: {err.get('msg')}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": " ".join(errors),
            "error_code": "INVALID_INPUT"
        }
    )


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/api/v1/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT
    }

# Include Routers
app.include_router(events_router, prefix="/api/v1")
app.include_router(registrations_router, prefix="/api/v1")
