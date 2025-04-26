from dataclasses import dataclass

from Chapter_4.TodoApp.todo_app.domain.entities.entity import Entity
from Chapter_4.TodoApp.todo_app.domain.value_objects import Priority, Deadline


@dataclass
class Task(Entity):
    # ... existing attributes ...

    @classmethod
    def create_urgent_task(cls, title: str, description: str, due_date: Deadline):
        return cls(title, description, due_date, Priority.HIGH)
