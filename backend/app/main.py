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
from app.models.registration import Registration, RegistrationStatus

def seed_sample_events():
    db = SessionLocal()
    try:
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
            ),
            Event(
                title="AI & Machine Learning Summit",
                description="Explore cutting-edge advancements in generative AI, LLMs, neural network architectures, and scalable ML infrastructure.",
                location="Grand Ballroom, Tech Center",
                start_time=now + timedelta(days=8),
                total_capacity=50
            ),
            Event(
                title="React Advanced Workshop",
                description="Deep dive into React Server Components, custom hooks, performance profiling, and advanced UI state management patterns.",
                location="Workshop Studio B",
                start_time=now + timedelta(days=10),
                total_capacity=2
            ),
            Event(
                title="Full Stack Development Workshop",
                description="Comprehensive hands-on training for building end-to-end web applications with modern APIs and cloud infrastructure.",
                location="Innovation Lab 204",
                start_time=now + timedelta(days=15),
                total_capacity=30
            ),
            Event(
                title="Cloud Computing & DevOps",
                description="Master Docker containerization, Kubernetes orchestration, CI/CD pipelines, and Infrastructure as Code on multi-cloud platforms.",
                location="Hall B, Enterprise Campus",
                start_time=now + timedelta(days=20),
                total_capacity=75
            ),
            Event(
                title="Cybersecurity Awareness Conference",
                description="Interactive security conference on threat modeling, zero-trust network security, and secure application development.",
                location="Security Center Auditorium",
                start_time=now + timedelta(days=25),
                total_capacity=20
            ),
            Event(
                title="Data Engineering Bootcamp",
                description="Master real-time data streaming pipelines with Apache Kafka, modern data warehousing, and scalable ETL processing.",
                location="Data Hub Room 301",
                start_time=now + timedelta(days=30),
                total_capacity=40
            ),
            Event(
                title="Open Source Community Meetup",
                description="Collaborative gathering for open-source maintainers, contributors, and developers to share projects and contribute to repositories.",
                location="Community Hub & Virtual Stream",
                start_time=now + timedelta(days=35),
                total_capacity=60
            )
        ]
        
        existing_titles = {e[0] for e in db.query(Event.title).all()}
        events_to_add = [e for e in sample_events if e.title not in existing_titles]
        if events_to_add:
            db.add_all(events_to_add)
            db.commit()

        # Seed registrations for React Advanced Workshop to demonstrate full/waitlisted state
        full_event = db.query(Event).filter(Event.title == "React Advanced Workshop").first()
        if full_event and db.query(Registration).filter(Registration.event_id == full_event.id).count() == 0:
            sample_regs = [
                Registration(
                    event_id=full_event.id,
                    full_name="Sarah Connor",
                    email="sarah.c@example.com",
                    status=RegistrationStatus.CONFIRMED
                ),
                Registration(
                    event_id=full_event.id,
                    full_name="John Doe",
                    email="john.d@example.com",
                    status=RegistrationStatus.CONFIRMED
                ),
                Registration(
                    event_id=full_event.id,
                    full_name="Alex Mercer",
                    email="alex.m@example.com",
                    status=RegistrationStatus.WAITLISTED
                )
            ]
            db.add_all(sample_regs)
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
