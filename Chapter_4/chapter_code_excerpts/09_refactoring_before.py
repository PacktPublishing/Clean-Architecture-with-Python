from dataclasses import dataclass, field
from typing import Optional

from Chapter_4.TodoApp.todo_app.domain.entities.entity import Entity
from Chapter_4.TodoApp.todo_app.domain.value_objects import (
    Deadline,
    Priority,
    TaskStatus,
)


# Before refactoring
@dataclass
class Task(Entity):
    title: str
    description: str
    due_date: Optional[Deadline] = None
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = field(default=TaskStatus.TODO, init=False)

    def mark_as_complete(self):
        self.status = TaskStatus.DONE
        # Sending an email notification - this violates domain purity
        self.send_completion_email()

    def send_completion_email(self):
        # Code to send an email notification
        print(f"Sending email: Task '{self.title}' has been completed.")
