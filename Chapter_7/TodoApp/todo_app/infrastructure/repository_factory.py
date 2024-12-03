"""
Factory functions for creating repositories based on configuration.
"""

from pathlib import Path
from typing import Tuple

from todo_app.application.repositories.project_repository import ProjectRepository
from todo_app.application.repositories.task_repository import TaskRepository
from todo_app.infrastructure.persistence.memory import (
    InMemoryTaskRepository,
    InMemoryProjectRepository,
)
from todo_app.infrastructure.persistence.file import (
    FileTaskRepository,
    FileProjectRepository,
)
from todo_app.infrastructure.config import Config


def create_repositories() -> Tuple[TaskRepository, ProjectRepository]:
    """
    Create and configure the appropriate repository implementations based on configuration.

    Returns:
        A tuple of (TaskRepository, ProjectRepository)
    """
    repo_type = Config.get_repository_type()

    if repo_type == "file":
        data_dir = Config.get_data_directory()
        return FileTaskRepository(data_dir), FileProjectRepository(data_dir)

    # Default to memory repositories
    return InMemoryTaskRepository(), InMemoryProjectRepository()
