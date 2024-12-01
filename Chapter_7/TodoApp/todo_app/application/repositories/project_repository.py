"""
This module defines the repository interface for Project entity persistence.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from todo_app.domain.entities.project import Project


class ProjectRepository(ABC):
    """Repository interface for Project entity persistence."""

    @abstractmethod
    def get(self, project_id: UUID) -> Project:
        """
        Retrieve a project by its ID.

        Args:
            project_id: The unique identifier of the project

        Returns:
            The requested Project entity

        Raises:
            ProjectNotFoundError: If no project exists with the given ID
        """
        pass

    @abstractmethod
    def save(self, project: Project) -> None:
        """
        Save a project to the repository.

        Args:
            project: The Project entity to save
        """
        pass

    @abstractmethod
    def delete(self, project_id: UUID) -> None:
        """
        Delete a project from the repository.

        Args:
            project_id: The unique identifier of the project to delete
        """
        pass

    @abstractmethod
    def get_inbox(self, inbox_name: str) -> Project:
        """
        Retrieve the INBOX project.

        Returns:
            The INBOX Project entity

        Raises:
            ProjectNotFoundError: If INBOX doesn't exist
        """
        pass
