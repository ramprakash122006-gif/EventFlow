from datetime import datetime, timedelta, timezone

def test_registration_happy_path(client):
    # 1. Create Event with capacity 2
    future_time = (datetime.now(timezone.utc) + timedelta(days=3)).isoformat()
    event_res = client.post("/api/v1/events", json={
        "title": "Clean Code Workshop",
        "location": "Room 101",
        "start_time": future_time,
        "total_capacity": 2
    })
    event_id = event_res.json()["id"]

    # 2. Register user 1
    reg_res = client.post(f"/api/v1/events/{event_id}/register", json={
        "full_name": "Alice Smith",
        "email": "alice@example.com"
    })
    assert reg_res.status_code == 200 or reg_res.status_code == 201
    reg_data = reg_res.json()
    assert reg_data["status"] == "CONFIRMED"
    assert reg_data["email"] == "alice@example.com"

    # 3. Check updated available seats count
    detail_res = client.get(f"/api/v1/events/{event_id}")
    assert detail_res.json()["available_seats"] == 1

def test_duplicate_registration_prevention(client):
    future_time = (datetime.now(timezone.utc) + timedelta(days=3)).isoformat()
    event_res = client.post("/api/v1/events", json={
        "title": "Python Deep Dive",
        "location": "Online",
        "start_time": future_time,
        "total_capacity": 5
    })
    event_id = event_res.json()["id"]

    # Register first time
    client.post(f"/api/v1/events/{event_id}/register", json={
        "full_name": "Bob Jones",
        "email": "bob@example.com"
    })

    # Register second time with different casing/spacing
    dup_res = client.post(f"/api/v1/events/{event_id}/register", json={
        "full_name": "Bob Jones Duplicate",
        "email": " BOB@EXAMPLE.COM "
    })
    assert dup_res.status_code == 409
    dup_data = dup_res.json()
    assert dup_data["error_code"] == "DUPLICATE_REGISTRATION"
    assert "already registered" in dup_data["detail"].lower()

def test_capacity_limit_and_waitlisting(client):
    future_time = (datetime.now(timezone.utc) + timedelta(days=3)).isoformat()
    event_res = client.post("/api/v1/events", json={
        "title": "Exclusive Seminar",
        "location": "VIP Suite",
        "start_time": future_time,
        "total_capacity": 1  # Only 1 seat
    })
    event_id = event_res.json()["id"]

    # User 1 occupies sole seat
    reg1 = client.post(f"/api/v1/events/{event_id}/register", json={
        "full_name": "First Attendee",
        "email": "first@example.com"
    })
    assert reg1.json()["status"] == "CONFIRMED"

    # User 2 attempts registration -> goes to waitlist
    reg2 = client.post(f"/api/v1/events/{event_id}/register", json={
        "full_name": "Second Attendee",
        "email": "second@example.com"
    })
    assert reg2.status_code == 200 or reg2.status_code == 201
    assert reg2.json()["status"] == "WAITLISTED"

    # Verify event metrics
    detail = client.get(f"/api/v1/events/{event_id}").json()
    assert detail["confirmed_count"] == 1
    assert detail["waitlisted_count"] == 1
    assert detail["available_seats"] == 0
    assert detail["is_full"] is True

def test_past_event_registration_rejection(client):
    past_time = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
    event_res = client.post("/api/v1/events", json={
        "title": "Yesterday Talk",
        "location": "Room 5",
        "start_time": past_time,
        "total_capacity": 10
    })
    event_id = event_res.json()["id"]

    reg_res = client.post(f"/api/v1/events/{event_id}/register", json={
        "full_name": "Late Commer",
        "email": "late@example.com"
    })
    assert reg_res.status_code == 400
    assert reg_res.json()["error_code"] == "PAST_EVENT_REGISTRATION"

def test_cancellation_and_auto_waitlist_promotion(client):
    future_time = (datetime.now(timezone.utc) + timedelta(days=3)).isoformat()
    event_res = client.post("/api/v1/events", json={
        "title": "Auto Promotion Test Event",
        "location": "Lab 1",
        "start_time": future_time,
        "total_capacity": 1
    })
    event_id = event_res.json()["id"]

    # User 1 registers (CONFIRMED)
    reg1 = client.post(f"/api/v1/events/{event_id}/register", json={
        "full_name": "User One",
        "email": "one@example.com"
    }).json()
    reg1_id = reg1["id"]

    # User 2 registers (WAITLISTED)
    reg2 = client.post(f"/api/v1/events/{event_id}/register", json={
        "full_name": "User Two",
        "email": "two@example.com"
    }).json()
    reg2_id = reg2["id"]
    assert reg2["status"] == "WAITLISTED"

    # User 1 cancels registration
    cancel_res = client.post(f"/api/v1/registrations/{reg1_id}/cancel")
    assert cancel_res.status_code == 200
    assert cancel_res.json()["status"] == "CANCELLED"

    # Verify User 2 was automatically promoted to CONFIRMED!
    event_regs = client.get(f"/api/v1/events/{event_id}/registrations").json()
    promoted_reg2 = next(r for r in event_regs if r["id"] == reg2_id)
    assert promoted_reg2["status"] == "CONFIRMED"

def test_cancel_already_cancelled_registration(client):
    future_time = (datetime.now(timezone.utc) + timedelta(days=3)).isoformat()
    event_res = client.post("/api/v1/events", json={
        "title": "Double Cancel Test",
        "location": "Room 2",
        "start_time": future_time,
        "total_capacity": 5
    })
    event_id = event_res.json()["id"]

    reg = client.post(f"/api/v1/events/{event_id}/register", json={
        "full_name": "User Three",
        "email": "three@example.com"
    }).json()
    reg_id = reg["id"]

    # First cancel
    client.post(f"/api/v1/registrations/{reg_id}/cancel")

    # Second cancel attempt
    second_cancel = client.post(f"/api/v1/registrations/{reg_id}/cancel")
    assert second_cancel.status_code == 400
    assert second_cancel.json()["error_code"] == "ALREADY_CANCELLED"
