from app import app

def test_create_task():
    client = app.test_client()
    response = client.post(
        "/api/tasks",
        json={
            "title": "Test Task",
            "description": "Testing API",
            "due_date": "2025-12-31"
        }
    )
    assert response.status_code == 201

def test_get_tasks():
    client = app.test_client()
    response = client.get("/api/tasks")
    assert response.status_code == 200
