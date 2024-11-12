"""
This module defines the repository interface for Task entity persistence.
"""

from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from Chapter_5.TodoApp.todo_app.domain.entities.task import Task


class TaskRepository(ABC):
    """Repository interface for Task entity persistence."""

    @abstractmethod
    def get(self, task_id: UUID) -> Task:
        """
        Retrieve a task by its ID.

        Args:
            task_id: The unique identifier of the task

        Returns:
            The requested Task entity

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        pass

    @abstractmethod
    def save(self, task: Task) -> None:
        """
        Save a task to the repository.

        Args:
            task: The Task entity to save
        """
        pass

    @abstractmethod
    def delete(self, task_id: UUID) -> None:
        """
        Delete a task from the repository.

        Args:
            task_id: The unique identifier of the task to delete
        """
        pass

    @abstractmethod
    def find_by_project(self, project_id: UUID) -> Sequence[Task]:
        """
        Find all tasks associated with a project.

        Args:
            project_id: The unique identifier of the project

        Returns:
            A sequence of Task entities belonging to the project
        """
        pass

    @abstractmethod
    def get_active_tasks(self) -> Sequence[Task]:
        """
        Retrieve all active tasks in the repository.

        Returns:
            A sequence of all active Tasks
        """
        pass
