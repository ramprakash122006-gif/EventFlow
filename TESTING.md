# EventFlow — Testing Documentation

## 1. Testing Overview

EventFlow uses automated testing at two levels:

- Backend API testing with Pytest
- End-to-End browser testing with Playwright

The purpose of the test suite is to verify the application's core business rules, API behavior, registration workflow, validation, capacity management, and frontend-backend integration.

---

## 2. Backend Testing

### Test Framework

The backend uses:

- Pytest
- FastAPI TestClient
- HTTPX
- SQLite test database

### Run Backend Tests

From the `backend` directory:

```bash
python -m pytest tests -v
Backend Test Result

The complete backend test suite contains 10 tests.

Result:

10 passed
Backend Tests Covered
Event Tests
Health check
Successful event creation
Invalid event capacity validation
Event listing
Registration Tests
Successful attendee registration
Duplicate registration prevention
Capacity limit and waitlisting
Past event registration rejection
Cancellation and automatic waitlist promotion
Preventing cancellation of an already cancelled registration
Business Rules Verified

The backend tests verify that:

Events can be created successfully.
Event capacity must be greater than zero.
Events can be retrieved through the API.
Users can register for future events.
A user cannot register twice for the same event using the same email.
Email comparison is case-insensitive.
Registrations exceeding event capacity are waitlisted.
Users cannot register for events that have already occurred.
Cancelling a confirmed registration automatically promotes the earliest waitlisted attendee.
A cancelled registration cannot be cancelled again.
3. End-to-End Testing
Test Framework

The frontend workflow is tested using:

Playwright
Chromium
Vite development server
FastAPI backend

The Playwright configuration uses:

Frontend: http://127.0.0.1:5173
Backend:  http://127.0.0.1:8000
Run E2E Tests

Make sure both the backend and frontend servers are running.

From the tests-e2e directory:

npx playwright test
E2E Test Result

The complete Playwright suite contains 4 tests.

Final result:

4 passed
E2E Tests Covered
1. Event List and Capacity Metrics

Verifies that:

The EventFlow branding is displayed.
Event cards are rendered.
The event list is accessible to the user.
2. Event Registration

Verifies that:

A user can select an available event.
The registration modal opens.
The user can enter their name and email.
Registration can be submitted successfully.
The application displays a confirmation or waitlist message.
3. Duplicate Registration

Verifies that:

A user can register initially.
A second registration using the same email is rejected.
Email matching is case-insensitive.
A clear "already registered" error is displayed.
4. Invalid Email Validation

Verifies that:

The registration modal accepts user input.
Invalid email addresses are rejected.
A clear validation message is displayed to the user.
4. Test Environment
Backend
Python 3.13.3
FastAPI
Uvicorn
Pytest
SQLite
Frontend
React
Vite
JavaScript
E2E
Playwright
Chromium
5. Final Test Status
Test Suite	Tests	Result
Backend Pytest	10	PASS
Playwright E2E	4	PASS
Total	14	PASS

The final verified state of the project is:

Backend:       10/10 passed
E2E:            4/4 passed
Total:         14/14 passed
6. Test Evidence

Screenshots demonstrating the successful test runs are included in the project documentation/screenshots folder.

Recommended evidence includes:

Backend Pytest terminal output showing 10 passed
Playwright terminal output showing 4 passed
EventFlow event list
Registration modal
Successful registration
Waitlist state
Duplicate registration error
Invalid email validation
7. Testing Conclusion

The automated test suites provide coverage for the application's main event-management and registration workflows.

The backend tests verify the core business rules and API behavior, while the Playwright tests verify that the most important user workflows operate correctly through the browser.

At the final verified stage:

14 automated tests passed successfully.
