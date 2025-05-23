from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from todo_app.domain.entities.entity import Entity
from todo_app.domain.value_objects import (
    Deadline,
    Priority,
    TaskStatus,
)


@dataclass
class Task(Entity):
    title: str
    description: str
    due_date: Optional[Deadline] = None
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = field(default=TaskStatus.TODO, init=False)

    def mark_as_complete(self):
        self.status = TaskStatus.DONE
        # No email sending here; this is now the responsibility of an outer layer


class TaskCompleteNotifier(ABC):
    @abstractmethod
    def notify_completion(self, task):
        pass


# This would be implemented in an outer layer
class EmailTaskCompleteNotifier(TaskCompleteNotifier):
    def notify_completion(self, task):
        print(f"Sending email: Task '{task.title}' has been completed.")
