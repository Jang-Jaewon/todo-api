from pydantic import BaseModel


class TodoItem(BaseModel):
    id: int
    content: str
    is_done: bool


class CreateTodoRequest(TodoItem):
    pass
