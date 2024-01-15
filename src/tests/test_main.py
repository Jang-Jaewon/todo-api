from database.orm import ToDo


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_get_todos(client, mocker):
    # order=ASE
    mocker.patch(
        "main.repository.get_todos",
        return_value=[
            ToDo(id=1, contents="content 1", is_done=True),
            ToDo(id=2, contents="content 2", is_done=False),
        ],
    )
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 1, "contents": "content 1", "is_done": True},
            {"id": 2, "contents": "content 2", "is_done": False},
        ]
    }

    # order=DESC
    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 2, "contents": "content 2", "is_done": False},
            {"id": 1, "contents": "content 1", "is_done": True},
        ]
    }
