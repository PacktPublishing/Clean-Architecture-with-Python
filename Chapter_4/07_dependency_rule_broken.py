from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from Chapter_4.TodoApp.todo_app.domain.entities.entity import Entity
from Chapter_4.TodoApp.todo_app.domain.entities.task import Task
from Chapter_4.TodoApp.todo_app.domain.value_objects import (
    TaskStatus,
    Deadline,
    Priority,
)


class DbConnection:
    pass


class UiComponent:
    pass


@dataclass
class TaskWithDatabase:
    """
    Violating the dependency rule via a db connection
    """

    title: str
    description: str
    db: DbConnection  # This violates the Dependency Rule
    due_date: Optional[Deadline] = None
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = field(default=TaskStatus.TODO, init=False)

    def mark_as_complete(self):
        self.status = TaskStatus.DONE
        self.db.update(self)


@dataclass
class ProjectWithUI(Entity):
    """
    Violating the dependency rule via a UI concern
    """

    name: str
    ui: UiComponent  # Violates the Dependency Rule
    description: str = ""
    _tasks: dict[UUID, Task] = field(default_factory=dict, init=False)

    def add_task(self, task: Task):
        self._tasks[task.id] = task
        self.ui.refresh()  # Violates the Dependency Rule
