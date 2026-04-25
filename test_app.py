import pytest
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, DATA_FILE


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_data = tmp_path / "todos.json"
    monkeypatch.setattr("app.DATA_FILE", str(test_data))
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"


def test_get_todos_empty(client):
    res = client.get("/api/todos")
    assert res.status_code == 200
    assert res.get_json() == []


def test_create_todo(client):
    res = client.post("/api/todos",
        data=json.dumps({"title": "Buy groceries"}),
        content_type="application/json")
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Buy groceries"
    assert data["completed"] is False
    assert "id" in data


def test_create_todo_missing_title(client):
    res = client.post("/api/todos",
        data=json.dumps({}),
        content_type="application/json")
    assert res.status_code == 400


def test_create_todo_empty_title(client):
    res = client.post("/api/todos",
        data=json.dumps({"title": "   "}),
        content_type="application/json")
    assert res.status_code == 400


def test_toggle_todo(client):
    create = client.post("/api/todos",
        data=json.dumps({"title": "Test task"}),
        content_type="application/json")
    todo_id = create.get_json()["id"]

    res = client.patch(f"/api/todos/{todo_id}",
        data=json.dumps({"completed": True}),
        content_type="application/json")
    assert res.status_code == 200
    assert res.get_json()["completed"] is True


def test_delete_todo(client):
    create = client.post("/api/todos",
        data=json.dumps({"title": "Delete me"}),
        content_type="application/json")
    todo_id = create.get_json()["id"]

    res = client.delete(f"/api/todos/{todo_id}")
    assert res.status_code == 200

    todos = client.get("/api/todos").get_json()
    assert not any(t["id"] == todo_id for t in todos)


def test_todo_not_found(client):
    res = client.patch("/api/todos/999999",
        data=json.dumps({"completed": True}),
        content_type="application/json")
    assert res.status_code == 404


def test_multiple_todos(client):
    for title in ["Task A", "Task B", "Task C"]:
        client.post("/api/todos",
            data=json.dumps({"title": title}),
            content_type="application/json")
    todos = client.get("/api/todos").get_json()
    assert len(todos) == 3
