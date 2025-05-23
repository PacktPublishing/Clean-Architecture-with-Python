from dataclasses import dataclass

from todo_app.domain.entities.entity import Entity


@dataclass
class Task(Entity):
    # ... existing attributes ...

    def __post_init__(self):
        if not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if len(self.description) > 500:
            raise ValueError("Task description cannot exceed 500 characters")