from typing import List

from pydantic import BaseModel


class TodoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    class Config:
        orm_mode = True


class ListTodoResponse(BaseModel):
    todos: List[TodoSchema]
