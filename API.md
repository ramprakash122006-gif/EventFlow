# EventFlow — API Documentation

## Base URL

```text
http://127.0.0.1:8000/api/v1
API Endpoints
Health Check

GET /health

Checks whether the backend is running.

Example response:

{
  "status": "healthy"
}
Events
Get All Events

GET /events

Returns the available events with capacity and registration metrics.

Example response:

[
  {
    "id": 1,
    "title": "Tech Innovation Summit 2026",
    "description": "Explore AI, Cloud Native, and Event-Driven Architecture.",
    "location": "Auditorium A",
    "start_time": "2026-08-17T11:48:35",
    "total_capacity": 3,
    "confirmed_count": 3,
    "waitlisted_count": 8,
    "available_seats": 0,
    "is_full": true
  }
]
Get Event Details

GET /events/{event_id}

Returns details and current registration metrics for a specific event.

Create Event

POST /events

Creates a new event.

Example request:

{
  "title": "React Workshop",
  "description": "Hands-on React workshop.",
  "location": "Workshop Room 102",
  "start_time": "2026-08-24T11:48:35",
  "total_capacity": 5
}

The event capacity must be greater than zero.

Registrations
Register for an Event

POST /events/{event_id}/register

Registers an attendee for an event.

Example request:

{
  "full_name": "Alice Smith",
  "email": "alice@example.com"
}

Possible registration statuses:

CONFIRMED
WAITLISTED

If seats are available, the registration is confirmed.

If the event is full, the attendee is placed on the waitlist.

Get Event Registrations

GET /events/{event_id}/registrations

Returns registrations associated with an event, including their current status.

Cancel Registration

POST /registrations/{registration_id}/cancel

Cancels an attendee's registration.

If the cancelled registration was confirmed and a waitlisted attendee exists, the earliest waitlisted attendee is automatically promoted to CONFIRMED.

Error Handling

The API uses HTTP status codes together with structured error responses.

Examples include:

Duplicate Registration
HTTP 409 Conflict
{
  "error_code": "DUPLICATE_REGISTRATION",
  "detail": "User is already registered for this event."
}
Past Event Registration
HTTP 400 Bad Request
{
  "error_code": "PAST_EVENT_REGISTRATION",
  "detail": "Cannot register for a past event."
}
Already Cancelled Registration
HTTP 400 Bad Request
{
  "error_code": "ALREADY_CANCELLED",
  "detail": "Registration has already been cancelled."
}
Validation Error

Invalid request data is rejected by FastAPI/Pydantic validation.

HTTP 422
Interactive API Documentation

When the backend is running, FastAPI provides interactive Swagger documentation at:

http://127.0.0.1:8000/docs

The Swagger interface can be used to inspect and manually test the available API endpoints.

Frontend Integration

The React frontend communicates with the backend through the /api/v1 endpoints.

During local development, Vite proxies /api requests to:

http://127.0.0.1:8000

This allows the frontend to communicate with the FastAPI backend without hardcoding the backend URL throughout the application.
