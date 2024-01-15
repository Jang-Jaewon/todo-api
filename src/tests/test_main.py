from fastapi.testclient import TestClient

from main import app

client = TestClient(app=app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_get_todos():
    # order=ASE
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 1, "contents": "content 1", "is_done": True},
            {"id": 2, "contents": "content 2", "is_done": False},
            {"id": 4, "contents": "content 4", "is_done": False},
            {"id": 5, "contents": "content 5", "is_done": False},
            {"id": 6, "contents": "content 6", "is_done": False},
            {"id": 7, "contents": "content 7", "is_done": True},
        ]
    }

    # order=DESC
    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 7, "contents": "content 7", "is_done": True},
            {"id": 6, "contents": "content 6", "is_done": False},
            {"id": 5, "contents": "content 5", "is_done": False},
            {"id": 4, "contents": "content 4", "is_done": False},
            {"id": 2, "contents": "content 2", "is_done": False},
            {"id": 1, "contents": "content 1", "is_done": True},
        ]
    }
