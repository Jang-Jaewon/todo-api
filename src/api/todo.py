from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException

from database.orm import ToDo
from database.repository import ToDoRepository
from schema.request import CreateTodoRequest
from schema.response import ToDoListSchema, ToDoSchema

router = APIRouter(prefix="/todos")


@router.get("", status_code=200)
def get_todos(
    order: str | None = None, todo_repo: ToDoRepository = Depends()
) -> ToDoListSchema:
    todos: List[ToDo] = todo_repo.get_todos()
    if order == "DESC":
        todos = todos[::-1]
    return ToDoListSchema(todos=[ToDoSchema.from_orm(todo) for todo in todos])


@router.post("", status_code=201)
def create_todos(request: CreateTodoRequest, todo_repo: ToDoRepository = Depends()):
    todo: ToDo = ToDo.create(request=request)
    todo: ToDo = todo_repo.create_todo(todo=todo)
    return ToDoSchema.from_orm(todo)


@router.get("/{todo_id}", status_code=200)
def get_todo(todo_id: int, todo_repo: ToDoRepository = Depends()) -> ToDoSchema:
    todo: ToDo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    return ToDoSchema.from_orm(todo)


@router.patch("/{todo_id}", status_code=200)
def update_todo(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
    todo_repo: ToDoRepository = Depends(),
):
    todo: ToDo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    todo.done() if is_done else todo.undone()
    todo: ToDo = todo_repo.update_todo(todo=todo)
    return ToDoSchema.from_orm(todo)


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, todo_repo: ToDoRepository = Depends()):
    todo: ToDo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    todo_repo.delete_todo(todo_id=todo_id)
