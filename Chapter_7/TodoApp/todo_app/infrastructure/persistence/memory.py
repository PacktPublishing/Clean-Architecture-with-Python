"""
In-memory repository implementations for demonstrating Interface Adapters patterns.

This is a preimptive view into the Framworks and Drivers layer.

This module provides basic in-memory implementations of repository interfaces to
demonstrate Clean Architecture principles without the complexity of a real database.
It shows:
- How repository interfaces from the Application layer are implemented
- How persistence concerns are kept separate from business logic
- Basic error handling at the storage boundary

These implementations will be replaced by actual database repositories in Chapter 7,
demonstrating how Clean Architecture enables swapping storage mechanisms while
maintaining core functionality.
"""

from typing import Dict, Sequence
from uuid import UUID, uuid4

from todo_app.domain.entities.task import Task
from todo_app.domain.entities.project import Project
from todo_app.domain.exceptions import InboxNotFoundError, TaskNotFoundError, ProjectNotFoundError
from todo_app.domain.value_objects import TaskStatus
from todo_app.application.repositories.task_repository import TaskRepository
from todo_app.application.repositories.project_repository import ProjectRepository


class InMemoryTaskRepository(TaskRepository):
    """
    In-memory implementation of TaskRepository for teaching Interface Adapters concepts.

    This class demonstrates how storage gateways work in Clean Architecture:
    - Implements interface defined by Application layer
    - Encapsulates storage details (in-memory dict in this case)
    - Maintains separation between storage and business logic
    - Handles storage-related errors

    While simplified, this implementation establishes patterns that will be used
    in actual database implementations.
    """

    def __init__(self):
        self._tasks: Dict[UUID, Task] = {}

    def get(self, task_id: UUID) -> Task:
        """Retrieve a task by ID or raise TaskNotFoundError."""
        if task := self._tasks.get(task_id):
            return task
        raise TaskNotFoundError(task_id)

    def save(self, task: Task) -> None:
        """Save or update a task."""
        self._tasks[task.id] = task

    def delete(self, task_id: UUID) -> None:
        """Delete a task if it exists."""
        self._tasks.pop(task_id, None)

    def find_by_project(self, project_id: UUID) -> Sequence[Task]:
        """Find all tasks belonging to a project."""
        return [task for task in self._tasks.values() if task.project_id == project_id]

    def get_active_tasks(self) -> Sequence[Task]:
        """Get all non-completed tasks."""
        return [task for task in self._tasks.values() if task.status != TaskStatus.DONE]


class InMemoryProjectRepository(ProjectRepository):
    """
    In-memory implementation of ProjectRepository for teaching Interface Adapters concepts.

    Similar to InMemoryTaskRepository, this class demonstrates gateway implementation
    patterns that will be used with actual databases in later chapters.
    """

    def __init__(self):
        self._projects: Dict[UUID, Project] = {}

    def get(self, project_id: UUID) -> Project:
        """Retrieve a project by ID or raise ProjectNotFoundError."""
        if project := self._projects.get(project_id):
            return project
        raise ProjectNotFoundError(project_id)

    def save(self, project: Project) -> None:
        """Save or update a project."""
        self._projects[project.id] = project

    def delete(self, project_id: UUID) -> None:
        """Delete a project if it exists."""
        self._projects.pop(project_id, None)

    def get_inbox(self, inbox_name: str) -> Project:
        for project in self._projects.values():
            if project.name == inbox_name:
                return project
        raise InboxNotFoundError()
