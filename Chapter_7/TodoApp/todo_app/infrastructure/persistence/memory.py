from typing import Dict, Optional, Sequence
from uuid import UUID
from logging import getLogger

from todo_app.domain.entities.project import Project
from todo_app.application.repositories.task_repository import TaskRepository
from todo_app.domain.entities.task import Task
from todo_app.domain.value_objects import TaskStatus, ProjectType
from todo_app.application.repositories.project_repository import ProjectRepository
from todo_app.domain.exceptions import InboxNotFoundError, ProjectNotFoundError, TaskNotFoundError

logger = getLogger(__name__)


class InMemoryTaskRepository(TaskRepository):
    """In-memory implementation of TaskRepository."""

    def __init__(self) -> None:
        self._tasks: Dict[UUID, Task] = {}

    def get(self, task_id: UUID) -> Task:
        """
        Retrieve a task by ID.

        Args:
            task_id: The unique identifier of the task

        Returns:
            The requested task

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        if task := self._tasks.get(task_id):
            return task
        raise TaskNotFoundError(task_id)

    def save(self, task: Task) -> None:
        """
        Save a task.

        Args:
            task: The task to save
        """
        logger.debug(f"Saving task {task.id} for project {task.project_id}")
        self._tasks[task.id] = task

    def delete(self, task_id: UUID) -> None:
        """
        Delete a task.

        Args:
            task_id: The unique identifier of the task to delete
        """
        self._tasks.pop(task_id, None)

    def find_by_project(self, project_id: UUID) -> Sequence[Task]:
        """
        Find all tasks belonging to a project.

        Args:
            project_id: The unique identifier of the project

        Returns:
            A sequence of tasks belonging to the project
        """
        return [task for task in self._tasks.values() if task.project_id == project_id]

    def get_active_tasks(self) -> Sequence[Task]:
        """
        Get all non-completed tasks.

        Returns:
            A sequence of all active tasks
        """
        return [task for task in self._tasks.values() if task.status != TaskStatus.DONE]


class InMemoryProjectRepository(ProjectRepository):
    """In-memory implementation of ProjectRepository."""

    def __init__(self) -> None:
        self._projects: Dict[UUID, Project] = {}
        self._task_repo: Optional[TaskRepository] = None
        self._initialize_inbox()

    def _initialize_inbox(self) -> None:
        """Initialize the INBOX project if it doesn't exist."""
        inbox = self._fetch_inbox()
        if not inbox:
            inbox = Project.create_inbox()
            self.save(inbox)

    def _fetch_inbox(self) -> Optional[Project]:
        """
        Find the INBOX project in the repository.

        Returns:
            The INBOX project if it exists, None otherwise
        """
        return next(
            (p for p in self._projects.values() if p.project_type == ProjectType.INBOX), None
        )

    def set_task_repository(self, task_repo: TaskRepository) -> None:
        """
        Set the task repository reference.

        Args:
            task_repo: The task repository instance
        """
        self._task_repo = task_repo

    def _load_project_tasks(self, project: Project) -> None:
        """
        Load tasks for a project.

        Args:
            project: The project to load tasks for
        """
        if not self._task_repo:
            return

        project._tasks.clear()
        for task in self._task_repo.find_by_project(project.id):
            project._tasks[task.id] = task

    def get(self, project_id: UUID) -> Project:
        """
        Retrieve a project by ID.

        Args:
            project_id: The unique identifier of the project

        Returns:
            The requested project

        Raises:
            ProjectNotFoundError: If no project exists with the given ID
        """
        if project := self._projects.get(project_id):
            self._load_project_tasks(project)
            return project
        raise ProjectNotFoundError(project_id)

    def get_all(self) -> list[Project]:
        """
        Retrieve all projects.

        Returns:
            A list of all projects with their tasks loaded
        """
        projects = list(self._projects.values())
        for project in projects:
            self._load_project_tasks(project)
        return projects

    def save(self, project: Project) -> None:
        """
        Save a project.

        Args:
            project: The project to save
        """
        self._projects[project.id] = project

    def delete(self, project_id: UUID) -> None:
        """
        Delete a project.

        Args:
            project_id: The unique identifier of the project to delete
        """
        self._projects.pop(project_id, None)

    def get_inbox(self) -> Project:
        """
        Get the INBOX project.

        Returns:
            The INBOX project

        Raises:
            InboxNotFoundError: If the INBOX project doesn't exist
        """
        inbox = self._fetch_inbox()
        if not inbox:
            raise InboxNotFoundError("The Inbox project was not found")
        return inbox
