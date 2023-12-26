from fastapi import FastAPI, Body
from typing import Dict
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}


class TodoItem(BaseModel):
    id: int
    content: str
    is_done: bool


class CreateTodoRequest(TodoItem):
    pass


todo_data: Dict[int, TodoItem] = {
    1: TodoItem(id=1, content="content 1", is_done=True),
    2: TodoItem(id=2, content="content 2", is_done=False),
    3: TodoItem(id=3, content="content 3", is_done=False),
}


@app.get("/todos")
def get_todos(order: str | None = None):
    result = list(todo_data.values())
    if order == "DESC":
        return result[::-1]
    return result


@app.post("/todos")
def create_todos(request: CreateTodoRequest):
    todo_data[request.id] = request.dict()
    return todo_data[request.id]


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    result = todo_data.get(todo_id, {})
    return result


@app.patch("/todos/{todo_id}")
def update_todo(
        todo_id: int,
        is_done: bool = Body(..., embed=True),
):
    result = todo_data.get(todo_id)
    print(result)
    if result:
        result.is_done = is_done
        return result
    return {}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    result = todo_data.pop(todo_id, {})
    return todo_data

