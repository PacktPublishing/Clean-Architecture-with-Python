from typing import Dict, Optional, Sequence
from uuid import UUID

from todo_app.domain.entities.project import Project
from todo_app.application.repositories.task_repository import TaskRepository
from todo_app.domain.entities.task import Task
from todo_app.domain.value_objects import TaskStatus
from todo_app.application.repositories.project_repository import ProjectRepository
from todo_app.domain.exceptions import InboxNotFoundError, ProjectNotFoundError, TaskNotFoundError
from todo_app.domain.value_objects import ProjectType


class InMemoryTaskRepository(TaskRepository):
    """In-memory implementation of TaskRepository."""

    def __init__(self):
        self._tasks: Dict[UUID, Task] = {}

    def get(self, task_id: UUID) -> Task:
        """Retrieve a task by ID."""
        if task := self._tasks.get(task_id):
            return task
        raise TaskNotFoundError(task_id)

    def save(self, task: Task) -> None:
        """Save a task."""
        print(f"Saving task {task.id} for project {task.project_id}")  # Debug
        self._tasks[task.id] = task

    def delete(self, task_id: UUID) -> None:
        """Delete a task."""
        self._tasks.pop(task_id, None)

    def find_by_project(self, project_id: UUID) -> Sequence[Task]:
        """Find all tasks belonging to a project."""
        tasks = [task for task in self._tasks.values() if task.project_id == project_id]
        print(f"Found {len(tasks)} tasks for project {project_id}")  # Debug
        for task in tasks:
            print(f"- Task: {task.title} (ID: {task.id})")  # Debug
        return tasks

    def get_active_tasks(self) -> Sequence[Task]:
        """Get all non-completed tasks."""
        return [task for task in self._tasks.values() if task.status != TaskStatus.DONE]


class InMemoryProjectRepository(ProjectRepository):
    """In-memory implementation of ProjectRepository."""

    def __init__(self):
        self._projects: dict[UUID, Project] = {}
        self._task_repo: Optional[TaskRepository] = None
        # Initialize INBOX at repository creation
        inbox = self._fetch_inbox()
        if not inbox:
            inbox = Project.create_inbox()
            self.save(inbox)

    def set_task_repository(self, task_repo: TaskRepository) -> None:
        """Set the task repository reference."""
        self._task_repo = task_repo

    def get(self, project_id: UUID) -> Project:
        """Retrieve a project by ID."""
        if project := self._projects.get(project_id):
            project._tasks.clear()  # Reset tasks
            # Load current tasks
            if self._task_repo:
                for task in self._task_repo.find_by_project(project_id):
                    project._tasks[task.id] = task
            return project
        raise ProjectNotFoundError(project_id)

    def get_all(self) -> list[Project]:
        """Retrieve all projects."""
        projects = list(self._projects.values())
        # Load tasks for each project
        if self._task_repo:
            for project in projects:
                project._tasks.clear()  # Reset tasks
                for task in self._task_repo.find_by_project(project.id):
                    project._tasks[task.id] = task
        return projects

    def save(self, project: Project) -> None:
        """Save a project."""
        self._projects[project.id] = project

    def delete(self, project_id: UUID) -> None:
        """Delete a project."""
        self._projects.pop(project_id, None)

    def _fetch_inbox(self) -> Optional[Project]:
        """Find the INBOX project."""
        return next(
            (p for p in self._projects.values() if p.project_type == ProjectType.INBOX), None
        )

    def get_inbox(self) -> Project:
        """Get the INBOX project."""
        inbox = self._fetch_inbox()
        if not inbox:
            raise InboxNotFoundError("The Inbox project was not found")
        return inbox
