# EventFlow — Event Registration & Seat Management System

EventFlow is a lightweight, production-grade Event Registration and Capacity Management System built with Python FastAPI, SQLAlchemy (SQLite), React + Vite, Pytest, and Playwright.

It was designed specifically for an internship hiring assessment to showcase real business rules, edge-case handling, clean architecture, and automated test coverage.

---
## Current Status

The application is fully functional in the local development environment.

- Backend tests: 10/10 passed
- Playwright E2E tests: 4/4 passed
- Frontend ↔ FastAPI integration: working
- Event capacity and waitlist logic: working
- Automatic waitlist promotion: working
- Duplicate registration prevention: working

---

## Key Features & Business Rules

1. **Real-time Seat Capacity Enforcement**: Each event has a maximum capacity. Registrations are automatically confirmed until capacity is reached, after which users are placed on a waitlist.
2. **Duplicate Registration Prevention**: Prevents the same email address from registering more than once for an event (case-insensitive email matching). Attempts return an explicit `409 Conflict` HTTP status code.
3. **Past Event Safeguard**: Prevents signups for past events with a `400 Bad Request` response.
4. **Auto-Promotion on Cancellation**: When a confirmed registration is cancelled, the system automatically promotes the earliest waitlisted registrant to `CONFIRMED`.
5. **Layered Clean Architecture**: Strict separation of concerns between API routing, input validation (Pydantic), business domain services, and database persistence (SQLAlchemy).
6. **Automated Testing Suite**: Full Pytest backend suite (unit & integration tests) and Playwright E2E browser automation tests.

---

## Tech Stack

- **Backend**: Python 3.10+, FastAPI, Pydantic v2, uvicorn
- **Database & ORM**: SQLite, SQLAlchemy 2.0
- **Frontend**: React 18, Vite, Vanilla CSS (Glassmorphism & dark mode aesthetics)
- **Testing**: Pytest, HTTPX (Backend), Playwright (E2E)

---

## Project Structure

```
eventflow/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI initialization, CORS, exception handlers & seed data
│   │   ├── config.py              # Environment variables (Pydantic BaseSettings)
│   │   ├── database.py            # SQLite engine & SQLAlchemy session setup
│   │   ├── models/                # SQLAlchemy ORM models (Event, Registration)
│   │   ├── schemas/               # Pydantic validation schemas
│   │   ├── services/              # Pure domain logic (EventService, RegistrationService)
│   │   ├── api/                   # FastAPI route handlers (/events, /registrations)
│   │   └── exceptions.py          # Custom domain exceptions
│   ├── tests/                     # Pytest suite
│   ├── requirements.txt           # Python dependencies
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/            # React UI components (EventCard, RegistrationModal, Header, etc.)
│   │   ├── services/              # API wrapper for FastAPI endpoints
│   │   ├── App.jsx                # Dashboard view & modal controllers
│   │   └── index.css              # Custom styling (CSS tokens, glassmorphism, responsive grid)
│   ├── package.json
│   └── vite.config.js
├── tests-e2e/                     # Playwright E2E automation tests
│   ├── playwright.config.js
│   └── registration.spec.js
└── README.md
```
---

## API Endpoints

### Health

- `GET /api/v1/health` — Health check

### Events

- `GET /api/v1/events` — List all events
- `GET /api/v1/events/{event_id}` — Get event details
- `POST /api/v1/events` — Create an event

### Registrations

- `POST /api/v1/events/{event_id}/register` — Register an attendee
- `GET /api/v1/events/{event_id}/registrations` — List registrations for an event
- `POST /api/v1/registrations/{registration_id}/cancel` — Cancel a registration and automatically promote the next waitlisted attendee
---

## Prerequisites

- **Python**: `3.10` or higher
- **Node.js**: `18.0` or higher
- **npm**: `9.0` or higher

---

## Quick Start Guide

### 1. Setup & Run Backend (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Create and activate a virtual environment
python -m venv .venv


# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI development server
uvicorn app.main:app --reload --port 8000
```

> **API Documentation**: Interactive Swagger docs will be available at `http://127.0.0.1:8000/docs`.

---

### 2. Setup & Run Frontend (React + Vite)

In a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```

> Open your browser and navigate to `http://localhost:5173`.

---

## Running Automated Tests

### Backend Tests (Pytest)

Run unit and integration tests covering business rules, capacity limits, duplicate checking, and waitlist auto-promotion:

```bash
cd backend
python -m pytest tests -v
```

### End-to-End Tests (Playwright)

Make sure both backend (`http://127.0.0.1:8000`) and frontend (`http://localhost:5173`) are running, then:

```bash
cd tests-e2e
npm install
npx playwright install chromium
npx playwright test
```
---

## Test Results

### Backend Tests

```text
10 passed

---


## Technical Interview Discussion Points

When explaining this project in a technical assessment interview, highlight:

1. **Domain Service Isolation**: Route controllers in `app/api/` do not perform database queries or inline calculations; all business rules live cleanly inside `RegistrationService` and `EventService`.
2. **Data Sanitization**: Pydantic validators automatically trim strings and convert email addresses to lowercase before reaching database query filters.
3. **Transaction Safety**: Seat availability checks and registration inserts occur within single database transactions to avoid race conditions.
4. **Auto-Promotion Mechanism**: Cancelling a confirmed registration immediately runs a query to promote the oldest waitlisted attendee to `CONFIRMED`.
5. **Standardized Error Contracts**: Domain exceptions map to standard JSON error payloads containing custom `error_code` fields for frontend consumption.
