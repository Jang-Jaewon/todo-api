from typing import List

from fastapi import Body, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import repository
from database.connection import get_db
from database.orm import ToDo
from database.repository import create_todo
from schema.request import CreateTodoRequest
from schema.response import ToDoListSchema, ToDoSchema

app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}


@app.get("/todos", status_code=200)
def get_todos(
    order: str | None = None, session: Session = Depends(get_db)
) -> ToDoListSchema:
    todos: List[ToDo] = repository.get_todos(session=session)
    if order == "DESC":
        todos = todos[::-1]
    return ToDoListSchema(todos=[ToDoSchema.from_orm(todo) for todo in todos])


@app.post("/todos", status_code=201)
def create_todos(request: CreateTodoRequest, session: Session = Depends(get_db)):
    todo: ToDo = ToDo.create(request=request)
    todo: ToDo = create_todo(session=session, todo=todo)
    return ToDoSchema.from_orm(todo)


@app.get("/todos/{todo_id}", status_code=200)
def get_todo(todo_id: int, session: Session = Depends(get_db)) -> ToDoSchema:
    todo: ToDo | None = repository.get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    return ToDoSchema.from_orm(todo)


@app.patch("/todos/{todo_id}", status_code=200)
def update_todo(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
    session: Session = Depends(get_db),
):
    todo: ToDo | None = repository.get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    todo.done() if is_done else todo.undone()
    todo: ToDo = repository.update_todo(session=session, todo=todo)
    return ToDoSchema.from_orm(todo)


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    session: Session = Depends(get_db),
):
    todo: ToDo | None = repository.get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    repository.delete_todo(session=session, todo_id=todo_id)
