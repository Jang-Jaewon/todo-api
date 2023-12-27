from typing import Dict, List

from fastapi import Body, FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.connection import get_db
from database import repository
from database.orm import ToDo

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


@app.get("/todos", status_code=200)
def get_todos(order: str | None = None, session: Session = Depends(get_db)):
    todos: List[ToDo] = repository.get_todos(session=session)
    if order == "DESC":
        return todos[::-1]
    return todos


@app.post("/todos", status_code=201)
def create_todos(request: CreateTodoRequest):
    todo_data[request.id] = request.dict()
    return todo_data[request.id]


@app.get("/todos/{todo_id}", status_code=200)
def get_todo(todo_id: int):
    todo = todo_data.get(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    return todo


@app.patch("/todos/{todo_id}", status_code=200)
def update_todo(todo_id: int, is_done: bool = Body(..., embed=True)):
    todo = todo_data.get(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    todo.is_done = is_done
    return todo


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    todo = todo_data.pop(todo_id, None)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    return
