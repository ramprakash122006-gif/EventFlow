from datetime import datetime, timedelta, timezone

def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_create_event_success(client):
    future_time = (datetime.now(timezone.utc) + timedelta(days=5)).isoformat()
    payload = {
        "title": " Pytest Conference 2026 ",
        "description": "Annual testing summit.",
        "location": "Main Stage",
        "start_time": future_time,
        "total_capacity": 5
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Pytest Conference 2026"
    assert data["total_capacity"] == 5
    assert data["confirmed_count"] == 0
    assert data["available_seats"] == 5
    assert data["is_full"] is False

def test_create_event_invalid_capacity(client):
    future_time = (datetime.now(timezone.utc) + timedelta(days=5)).isoformat()
    payload = {
        "title": "Invalid Event",
        "location": "Room 1",
        "start_time": future_time,
        "total_capacity": 0  # Invalid capacity <= 0
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == 422

def test_list_events(client):
    future_time = (datetime.now(timezone.utc) + timedelta(days=5)).isoformat()
    client.post("/api/v1/events", json={
        "title": "Event 1",
        "location": "Loc 1",
        "start_time": future_time,
        "total_capacity": 10
    })

    response = client.get("/api/v1/events")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
