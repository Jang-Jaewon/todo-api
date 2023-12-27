from typing import List

from sqlalchemy import Select
from sqlalchemy.orm import Session

from database.orm import ToDo


def get_todos(session: Session) -> List[ToDo]:
    return list(session.scalars(Select(ToDo)))
