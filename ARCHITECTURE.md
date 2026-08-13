# EventFlow — System Architecture

## 1. Overview

EventFlow is a lightweight Event Registration and Seat Management System.

The application allows users to:

- View available events
- View event capacity and registration metrics
- Register for an event
- Receive a confirmed registration when seats are available
- Join a waitlist when an event is full
- Prevent duplicate registrations using email addresses
- Prevent registration for past events
- Automatically promote the earliest waitlisted attendee when a confirmed registration is cancelled

The system is implemented using a layered architecture that separates the frontend, API layer, business logic, validation, and database persistence.

---

## 2. Architecture Diagram

The high-level architecture is:

```text
┌───────────────────────────────────────────────┐
│                  User / Browser               │
└──────────────────────┬────────────────────────┘
                       │
                       │ HTTP
                       ▼
┌───────────────────────────────────────────────┐
│             React + Vite Frontend             │
│                                               │
│  App.jsx                                      │
│  ├── Header                                   │
│  ├── EventCard                                │
│  ├── CapacityBadge                            │
│  ├── RegistrationModal                        │
│  ├── RegistrationsListModal                   │
│  └── Toast                                    │
│                                               │
│  services/api.js                              │
└──────────────────────┬────────────────────────┘
                       │
                       │ /api/v1/*
                       │
                       ▼
┌───────────────────────────────────────────────┐
│              FastAPI Backend                  │
│                                               │
│  API Routes                                   │
│  ├── events.py                                │
│  └── registrations.py                         │
│                                               │
│  Pydantic Schemas                              │
│  ├── event.py                                 │
│  └── registration.py                          │
│                                               │
│  Domain Services                              │
│  ├── event_service.py                         │
│  └── registration_service.py                  │
│                                               │
│  Custom Exceptions                             │
└──────────────────────┬────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────┐
│              SQLAlchemy ORM                  │
│                                               │
│  Event Model                                  │
│  Registration Model                           │
└──────────────────────┬────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────┐
│                 SQLite Database               │
└───────────────────────────────────────────────┘
3. Technology Stack
Frontend
React

React is used to build the user interface and divide the application into reusable components.

The frontend contains components such as:

Header
EventCard
CapacityBadge
RegistrationModal
RegistrationsListModal
Toast
Vite

Vite provides the frontend development server and build tooling.

The development server runs on:

http://localhost:5173
Vanilla CSS

The project uses custom CSS for:

Responsive layouts
Event cards
Modal dialogs
Capacity indicators
Dark/glassmorphism visual styling
Form elements
Responsive behavior
4. Backend Architecture

The backend is implemented using Python and FastAPI.

The backend development server runs on:

http://127.0.0.1:8000

The API is organized under:

/api/v1

The backend follows a layered architecture.

API Routes
    ↓
Pydantic Schemas
    ↓
Domain Services
    ↓
SQLAlchemy Models
    ↓
SQLite Database

This separation prevents HTTP request handling from becoming tightly coupled with database and business logic.

5. Backend Project Structure

The relevant backend structure is:

backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── exceptions.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   ├── events.py
│   │   └── registrations.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── event.py
│   │   └── registration.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── event.py
│   │   └── registration.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── event_service.py
│       └── registration_service.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_events.py
│   └── test_registrations.py
│
└── requirements.txt
6. Application Entry Point

The main FastAPI application is initialized in:

backend/app/main.py

The main application is responsible for application initialization and backend configuration such as:

FastAPI application creation
API registration
CORS configuration
Exception handling
Database/application startup behavior
Seed/demo event data

The application exposes the API under the /api/v1 namespace.

7. API Layer

API route handlers are located in:

backend/app/api/

The main route modules are:

events.py
registrations.py

The API layer is responsible for:

Receiving HTTP requests
Validating request input through schemas
Calling the appropriate service
Returning HTTP responses
Translating domain errors into API error responses

The route layer does not contain the main event registration business rules.

This keeps business logic inside the service layer.

8. Event API

Event-related routes are implemented in:

backend/app/api/events.py

The event API supports operations such as:

Health Check
GET /api/v1/health

Used to verify that the backend is healthy.

List Events
GET /api/v1/events

Returns the available events together with registration metrics.

Example response information includes:

title
description
location
start_time
total_capacity
id
confirmed_count
waitlisted_count
available_seats
is_full
created_at
Event Details
GET /api/v1/events/{event_id}

Returns details and capacity information for a specific event.

Create Event
POST /api/v1/events

Creates a new event.

The event creation logic validates important input such as event capacity and event timing.

Event Registrations
GET /api/v1/events/{event_id}/registrations

Returns registrations associated with an event.

9. Registration API

Registration-related routes are implemented in:

backend/app/api/registrations.py
Register for Event
POST /api/v1/events/{event_id}/register

The endpoint receives attendee information such as:

{
  "full_name": "Alice Smith",
  "email": "alice@example.com"
}

The registration service then determines whether the attendee should be:

CONFIRMED

or:

WAITLISTED

depending on the event's available capacity.

Cancel Registration
POST /api/v1/registrations/{registration_id}/cancel

Cancels an existing registration.

If the cancelled registration was confirmed and a waitlisted attendee exists, the system automatically promotes the earliest waitlisted attendee.

10. Validation Layer

Request and response schemas are located in:

backend/app/schemas/

The schemas use Pydantic.

Main schema modules include:

event.py
registration.py

The validation layer is responsible for:

.Validating incoming request data
.Enforcing required fields
.Validating event capacity
.Validating email input
.Normalizing user input
.Providing structured validation errors

For example, event capacity must be greater than zero.

Invalid input results in an appropriate validation response rather than reaching the business logic with invalid data.

11. Service Layer

Business logic is isolated in:

backend/app/services/

The main services are:

event_service.py
registration_service.py

This is an important architectural decision in EventFlow.

The API routes are intentionally kept thin.

Instead of performing registration calculations directly inside a route handler:

API Route
    ↓
RegistrationService
    ↓
Database

This makes the business rules easier to:

Test
Maintain
Reuse
Reason about
Change independently from HTTP handling
12. Event Service

The event service handles event-related domain operations.

Responsibilities include:

Creating events
Retrieving events
Retrieving event details
Calculating event registration metrics
Determining available capacity
Determining whether an event is full

The event response exposes useful calculated information:

confirmed_count
waitlisted_count
available_seats
is_full

For example:

Capacity = 5
Confirmed = 3

Available seats = 5 - 3
                = 2

Therefore:

available_seats = 2
is_full = false
13. Registration Service

The registration service contains the primary registration business rules.

Responsibilities include:

Registering attendees
Checking duplicate registrations
Checking whether an event is in the past
Checking event capacity
Confirming registrations
Adding registrations to the waitlist
Cancelling registrations
Automatically promoting waitlisted attendees

The main decision flow is:

Registration Request
        │
        ▼
Validate attendee data
        │
        ▼
Does event exist?
        │
        ▼
Is event in the past?
        │
        ├── YES → Reject
        │
        ▼
Is email already registered?
        │
        ├── YES → 409 Conflict
        │
        ▼
Is capacity available?
        │
        ├── YES → CONFIRMED
        │
        └── NO  → WAITLISTED
14. Capacity Management

EventFlow enforces event capacity at the business-logic level.

For an event with:

total_capacity = 3

the system can have:

confirmed_count = 3
waitlisted_count = 8
available_seats = 0
is_full = true

When capacity is available:

available_seats > 0

a new registration becomes:

CONFIRMED

When capacity is exhausted:

available_seats = 0

new registrations become:

WAITLISTED

This ensures that the number of confirmed registrations does not exceed the event's configured capacity.

15. Waitlist Management

The waitlist is used when an event has no remaining confirmed seats.

Example:

Event capacity: 1

User A → CONFIRMED
User B → WAITLISTED
User C → WAITLISTED

If User A cancels:

User A → CANCELLED
User B → CONFIRMED
User C → WAITLISTED

The earliest eligible waitlisted attendee is promoted automatically.

This allows EventFlow to maintain the event's capacity while providing a predictable waitlist ordering.

16. Automatic Waitlist Promotion

Cancellation follows this process:

Confirmed Registration
        │
        ▼
Cancellation Request
        │
        ▼
Registration → CANCELLED
        │
        ▼
Find earliest WAITLISTED registration
        │
        ▼
Promote to CONFIRMED

This operation is performed by the registration business logic rather than by the frontend.

The frontend only displays the resulting state.

This ensures that the business rule is consistently enforced regardless of how the API is called.

17. Duplicate Registration Prevention

EventFlow prevents the same attendee email address from registering multiple times for the same event.

Email comparison is case-insensitive and normalized.

For example:

alice@example.com

and:

 ALICE@EXAMPLE.COM

are treated as the same email address.

A duplicate registration returns:

409 Conflict

with a domain-specific error code:

DUPLICATE_REGISTRATION

This allows the frontend to display a meaningful error message to the user.

18. Past Event Protection

Users cannot register for events that have already started.

The registration service checks the event's start time before creating a registration.

If the event is in the past, registration is rejected with:

400 Bad Request

and an error code such as:

PAST_EVENT_REGISTRATION

This rule is enforced in the backend rather than relying on the frontend to disable the registration button.

Therefore, the rule remains effective even if someone calls the API directly.

19. Registration Cancellation

Cancellation is handled through:

POST /api/v1/registrations/{registration_id}/cancel

The cancellation workflow checks the current registration status.

If a registration is already cancelled, another cancellation attempt is rejected rather than silently changing the state again.

The system returns an error code:

ALREADY_CANCELLED

This makes registration state transitions explicit and predictable.

20. Database Layer

Database configuration is located in:

backend/app/database.py

EventFlow uses:

SQLite

with:

SQLAlchemy 2.0

SQLAlchemy provides the ORM layer between Python business objects and database records.

The basic persistence flow is:

Python Service
      ↓
SQLAlchemy ORM
      ↓
SQLite

This keeps SQL/database implementation details out of the API route handlers.

21. Database Models

The database models are located in:

backend/app/models/

Main models:

event.py
registration.py

Conceptually, the relationship is:

Event
 │
 │ 1
 │
 ├───────────────┐
 │               │
 │               │
 ▼               ▼
Registration  Registration

One event can have many registrations.

Each registration belongs to an event.

22. Event Entity

An event contains information such as:

id
title
description
location
start_time
total_capacity
created_at

The event is the main resource around which registration and capacity management operate.

Derived registration metrics include:

confirmed_count
waitlisted_count
available_seats
is_full

These metrics allow the frontend to present the current event state to the user.

23. Registration Entity

A registration represents an attendee's participation request for an event.

Relevant information includes:

id
event_id
full_name
email
status

Registration status represents the current state of the attendee.

The main states used by EventFlow are:

CONFIRMED
WAITLISTED
CANCELLED

The state changes according to business rules.

Example:

New registration
      ↓
CONFIRMED

or

New registration
      ↓
WAITLISTED

Confirmed
      ↓
CANCELLED

WAITLISTED
      ↓
CONFIRMED
24. Frontend Architecture

The frontend is located in:

frontend/

The main application entry points are:

src/main.jsx
src/App.jsx

The frontend is component-based.

App
│
├── Header
│
├── EventCard
│   └── CapacityBadge
│
├── RegistrationModal
│
├── RegistrationsListModal
│
└── Toast

Each component has a focused responsibility.

25. Event Card

The event card component is:

frontend/src/components/EventCard.jsx

It presents event information such as:

Event title
Description
Location
Start time
Capacity
Availability
Registration state

The component also provides the registration interaction.

The UI uses the backend's event metrics to communicate whether an event has available seats or is full.

26. Registration Modal

The registration modal is:

frontend/src/components/RegistrationModal.jsx

It collects attendee information:

Full Name
Email

The modal communicates with the backend through the API service.

Successful registrations display a success state.

Backend errors such as duplicate registration are displayed to the user through the modal's error state.

27. API Service Layer in Frontend

Frontend API communication is centralized in:

frontend/src/services/api.js

The API base path is:

/api/v1

The service provides functions for operations such as:

getEvents()
getEventDetail(id)
registerForEvent(eventId, payload)
createEvent(payload)
cancelRegistration(registrationId)

This keeps HTTP request logic out of the React components.

The components call the API service instead of directly implementing fetch requests throughout the UI.

28. Frontend-to-Backend Communication

During local development, Vite proxies /api requests to the FastAPI backend.

The frontend configuration is:

frontend/vite.config.js

The proxy target is:

http://127.0.0.1:8000

Therefore a frontend request such as:

/api/v1/events

is forwarded to:

http://127.0.0.1:8000/api/v1/events

The browser can therefore communicate with the backend without hard-coding the backend server into every API request.

29. Error Handling

The backend uses standardized error responses.

The frontend API service contains centralized response handling in:

frontend/src/services/api.js

The response handler checks:

HTTP status
JSON response
detail
error_code

This allows domain-specific errors to be converted into meaningful frontend messages.

Examples include:

DUPLICATE_REGISTRATION
PAST_EVENT_REGISTRATION
ALREADY_CANCELLED

The approach prevents each React component from implementing its own HTTP error parsing logic.

30. Testing Architecture

EventFlow contains two levels of automated testing.

                Testing
                   │
          ┌────────┴────────┐
          │                 │
       Backend             E2E
       Pytest           Playwright
          │                 │
          ▼                 ▼
      FastAPI/API       Real Browser
      Business Rules     User Flows
31. Backend Tests

Backend tests are located in:

backend/tests/

The suite includes:

test_events.py
test_registrations.py

The backend test suite verifies:

Health endpoint
Event creation
Invalid event capacity
Event listing
Successful registration
Duplicate registration prevention
Capacity limits
Waitlisting
Past-event rejection
Cancellation
Automatic waitlist promotion
Repeated cancellation prevention

The current verified result is:

10 passed
32. End-to-End Tests

Browser-level tests are located in:

tests-e2e/

The main test file is:

registration.spec.js

Playwright tests cover important user-facing workflows including:

Viewing the EventFlow event list
Registering for an available event
Confirming the registration success state
Preventing duplicate email registration
Displaying invalid email validation errors

The verified current result is:

4 passed
33. Test Architecture

The test layers provide different levels of confidence.

Backend Tests

Backend tests directly exercise the API and business rules.

They are useful for verifying:

Business Logic
API Behavior
Validation
Database Operations
State Transitions
Playwright Tests

Playwright verifies the complete browser flow:

Browser
   ↓
React UI
   ↓
Vite Proxy
   ↓
FastAPI
   ↓
Database

This provides confidence that the frontend and backend work together as an integrated application.

34. Configuration

Configuration is handled through:

backend/app/config.py

Environment-specific values can be supplied using environment variables.

The repository contains:

backend/.env.example

while actual environment files are excluded from version control.

This avoids committing environment-specific or sensitive configuration to the repository.

35. Repository Structure

The complete project structure is:

eventflow/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_events.py
│   │   └── test_registrations.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── tests-e2e/
│   ├── playwright.config.js
│   ├── registration.spec.js
│   └── package.json
│
├── docs/
│   └── ARCHITECTURE.md
│
├── .gitignore
└── README.md
36. Key Architectural Decisions
36.1 Layered Backend Architecture

The backend separates:

Routes
Schemas
Services
Models
Database

This prevents the API layer from becoming responsible for all application behavior.

36.2 Business Rules in Services

Registration rules are implemented in the registration service instead of the React frontend.

This means rules such as:

Capacity enforcement
Duplicate prevention
Past-event rejection
Waitlist promotion

remain enforced even when the API is called directly.

36.3 Centralized Frontend API Communication

The frontend API calls are centralized in:

frontend/src/services/api.js

This makes the frontend easier to maintain and provides a single location for HTTP response and error handling.

36.4 Automated Testing

Both backend and browser-level tests are included.

This provides confidence at two levels:

Business Logic
      +
Complete User Experience
37. End-to-End Data Flow

A typical registration request follows this complete path:

1. User opens EventFlow
          │
          ▼
2. React loads event list
          │
          ▼
3. api.js requests /api/v1/events
          │
          ▼
4. Vite proxies request to FastAPI
          │
          ▼
5. FastAPI event route receives request
          │
          ▼
6. Event service retrieves event information
          │
          ▼
7. SQLAlchemy reads SQLite database
          │
          ▼
8. Event metrics are calculated
          │
          ▼
9. JSON response returned to React
          │
          ▼
10. EventCard displays event
          │
          ▼
11. User clicks Register
          │
          ▼
12. RegistrationModal collects details
          │
          ▼
13. api.js sends POST registration request
          │
          ▼
14. FastAPI registration route receives request
          │
          ▼
15. RegistrationService validates business rules
          │
          ├── Duplicate → Reject
          ├── Past event → Reject
          ├── Capacity available → CONFIRMED
          └── Event full → WAITLISTED
          │
          ▼
16. SQLAlchemy persists registration
          │
          ▼
17. API returns registration result
          │
          ▼
18. React displays success/error state
38. Cancellation Data Flow

Cancellation follows:

User / API Client
       │
       ▼
POST /registrations/{id}/cancel
       │
       ▼
FastAPI Registration Route
       │
       ▼
RegistrationService
       │
       ▼
Check registration state
       │
       ├── Already CANCELLED
       │       ↓
       │     Error
       │
       ▼
Mark registration CANCELLED
       │
       ▼
Was registration CONFIRMED?
       │
       ├── NO → Finish
       │
       ▼
Find earliest WAITLISTED attendee
       │
       ├── None → Finish
       │
       ▼
Promote attendee to CONFIRMED
       │
       ▼
Persist changes
       │
       ▼
Return updated registration
39. Security and Data Handling Considerations

The current architecture keeps environment configuration separate from source code through environment variables and .env.example.

The application also performs backend validation rather than trusting frontend validation alone.

Important business operations are therefore validated server-side.

For a production deployment, additional security controls could be introduced, such as:

Authentication and authorization
Rate limiting
HTTPS
Stronger database configuration
Production-grade database infrastructure
Audit logging
More extensive input security policies

These are outside the current lightweight EventFlow implementation.

40. Scalability Considerations

The current application uses SQLite, which is appropriate for a lightweight project and assessment environment.

The architecture keeps business logic separated from persistence, making future migration to another relational database easier.

For a larger deployment, the database layer could be moved to a production database such as PostgreSQL while keeping the API and service architecture largely unchanged.

Similarly, the frontend can continue communicating through the same API contract.

The main architectural benefit is that the business logic is not tightly coupled to the React UI.

41. Architecture Summary

EventFlow follows a layered architecture:

┌─────────────────────┐
│      React UI       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Frontend API      │
│      Service        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    FastAPI Routes   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Pydantic Schemas  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Domain Services   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  SQLAlchemy Models  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       SQLite        │
└─────────────────────┘

The architecture is designed around separation of concerns, testability, clear business rules, and a straightforward path from the browser to the database.

The most important domain behavior — capacity enforcement, duplicate prevention, past-event protection, cancellation and automatic waitlist promotion — is handled by the backend service layer rather than being dependent on frontend behavior.
