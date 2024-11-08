from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

from Chapter_4.TodoApp.todo_app.domain.entities.entity import Entity
from Chapter_4.TodoApp.todo_app.domain.entities.task import Task
from Chapter_5.ToDoApp.todo_app.domain.value_objects import (
    TaskStatus,
    ProjectStatus,
)


@dataclass
class Project(Entity):
    """A project containing multiple tasks."""

    name: str
    description: str = ""
    status: ProjectStatus = field(default=ProjectStatus.ACTIVE, init=False)
    completed_at: Optional[datetime] = field(default=None, init=False)
    completion_notes: Optional[str] = field(default=None, init=False)
    _tasks: dict[UUID, Task] = field(default_factory=dict, init=False)

    def add_task(self, task: Task) -> None:
        """Add a task to the project."""
        if self.status == ProjectStatus.COMPLETED:
            raise ValueError("Cannot add tasks to a completed project")
        self._tasks[task.id] = task
        task.project_id = self.id

    def remove_task(self, task_id: UUID) -> None:
        """Remove a task from the project."""
        if task := self._tasks.pop(task_id, None):
            task.project_id = None

    def get_task(self, task_id: UUID) -> Optional[Task]:
        """Get a task by its ID."""
        return self._tasks.get(task_id)

    @property
    def tasks(self) -> list[Task]:
        """Get all tasks in the project."""
        return list(self._tasks.values())

    @property
    def incomplete_tasks(self) -> list[Task]:
        """Get all incomplete tasks in the project."""
        return [task for task in self.tasks if task.status != TaskStatus.DONE]

    def mark_completed(self, notes: Optional[str] = None) -> None:
        """
        Mark the project as completed.

        Args:
            notes: Optional completion notes

        Raises:
            ValueError: If the project has incomplete tasks or is already completed
        """
        if self.status == ProjectStatus.COMPLETED:
            raise ValueError("Project is already completed")

        if self.incomplete_tasks:
            raise ValueError("Cannot complete project with incomplete tasks")

        self.status = ProjectStatus.COMPLETED
        self.completed_at = datetime.now()
        self.completion_notes = notes
