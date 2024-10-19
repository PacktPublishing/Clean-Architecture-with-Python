from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from Chapter_4.TodoApp.todo_app.domain.entities.entity import Entity
from Chapter_4.TodoApp.todo_app.domain.entities.task import Task


@dataclass
class Project(Entity):
    name: str
    description: str = ""
    _tasks: dict[UUID, Task] = field(default_factory=dict, init=False)

    def add_task(self, task: Task) -> None:
        self._tasks[task.id] = task

    def remove_task(self, task_id: UUID) -> None:
        self._tasks.pop(task_id, None)

    def get_task(self, task_id: UUID) -> Optional[Task]:
        return self._tasks.get(task_id)

    @property
    def tasks(self) -> list[Task]:
        return list(self._tasks.values())