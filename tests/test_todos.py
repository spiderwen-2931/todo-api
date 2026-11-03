import pytest
from fastapi.testclient import TestClient
from app.main import app
import app.crud as crud

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_store():
    """Reset the in-memory store before each test for isolation."""
    crud._reset()
    yield


# ── Health Check ───────────────────────────────────────────────────────────────

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "todo-api"}


# ── Create TODO ────────────────────────────────────────────────────────────────

def test_create_todo_basic():
    payload = {"title": "Buy groceries"}
    response = client.post("/todos/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Buy groceries"
    assert data["completed"] is False
    assert data["description"] is None


def test_create_todo_with_all_fields():
    payload = {"title": "Read a book", "description": "Finish Clean Code", "completed": True}
    response = client.post("/todos/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Read a book"
    assert data["description"] == "Finish Clean Code"
    assert data["completed"] is True


def test_create_todo_empty_title_fails():
    response = client.post("/todos/", json={"title": ""})
    assert response.status_code == 422  # Validation error


# ── List TODOs ─────────────────────────────────────────────────────────────────

def test_list_todos_empty():
    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_todos_multiple():
    client.post("/todos/", json={"title": "Task 1"})
    client.post("/todos/", json={"title": "Task 2"})
    response = client.get("/todos/")
    assert response.status_code == 200
    assert len(response.json()) == 2


# ── Get single TODO ────────────────────────────────────────────────────────────

def test_get_todo_by_id():
    client.post("/todos/", json={"title": "Single task"})
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Single task"


def test_get_todo_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


# ── Update TODO ────────────────────────────────────────────────────────────────

def test_update_todo_title():
    client.post("/todos/", json={"title": "Old title"})
    response = client.put("/todos/1", json={"title": "New title"})
    assert response.status_code == 200
    assert response.json()["title"] == "New title"


def test_update_todo_mark_completed():
    client.post("/todos/", json={"title": "Pending task"})
    response = client.put("/todos/1", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_update_todo_not_found():
    response = client.put("/todos/999", json={"title": "Ghost"})
    assert response.status_code == 404


# ── Delete TODO ────────────────────────────────────────────────────────────────

def test_delete_todo():
    client.post("/todos/", json={"title": "To delete"})
    response = client.delete("/todos/1")
    assert response.status_code == 204


def test_delete_todo_removes_from_list():
    client.post("/todos/", json={"title": "To delete"})
    client.delete("/todos/1")
    response = client.get("/todos/")
    assert response.json() == []


def test_delete_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == 404
