"""
JSON file-based repository implementation.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence
from uuid import UUID

from todo_app.domain.entities.task import Task
from todo_app.domain.entities.project import Project
from todo_app.domain.exceptions import TaskNotFoundError, ProjectNotFoundError, InboxNotFoundError
from todo_app.domain.value_objects import ProjectType, TaskStatus, ProjectStatus, Priority, Deadline
from todo_app.application.repositories.task_repository import TaskRepository
from todo_app.application.repositories.project_repository import ProjectRepository


class JsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for domain objects."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, (TaskStatus, ProjectStatus, Priority)):
            return obj.name
        return super().default(obj)


class FileTaskRepository(TaskRepository):
    """JSON file-based implementation of TaskRepository."""

    def __init__(self, data_dir: Path):
        self.tasks_file = data_dir / "tasks.json"
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Create the tasks file if it doesn't exist."""
        if not self.tasks_file.exists():
            self.tasks_file.write_text("[]")

    def _load_tasks(self) -> list[Dict[str, Any]]:
        """Load all tasks from the JSON file."""
        return json.loads(self.tasks_file.read_text())

    def _save_tasks(self, tasks: list[Dict[str, Any]]) -> None:
        """Save tasks to the JSON file."""
        self.tasks_file.write_text(json.dumps(tasks, indent=2, cls=JsonEncoder))

    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """Convert a Task entity to a dictionary for JSON storage."""
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "project_id": task.project_id,
            "due_date": task.due_date.due_date if task.due_date else None,
            "priority": task.priority.name,
            "status": task.status.name,
            "completed_at": task.completed_at,
            "completion_notes": task.completion_notes,
        }

    def _dict_to_task(self, data: Dict[str, Any]) -> Task:
        """Convert a dictionary to a Task entity."""
        # Create task with required attributes
        task = Task(
            title=data["title"],
            description=data["description"],
            project_id=UUID(data["project_id"]),
            priority=Priority[data["priority"]],
        )

        # Set additional attributes
        if data["due_date"]:
            task.due_date = Deadline(datetime.fromisoformat(data["due_date"]))
        task.status = TaskStatus[data["status"]]
        if data["completed_at"]:
            task.completed_at = datetime.fromisoformat(data["completed_at"])
        task.completion_notes = data["completion_notes"]

        # Explicitly set ID to maintain consistency
        task.id = UUID(data["id"])

        return task

    def get(self, task_id: UUID) -> Task:
        """Retrieve a task by ID."""
        tasks = self._load_tasks()
        for task_data in tasks:
            if UUID(task_data["id"]) == task_id:
                return self._dict_to_task(task_data)
        raise TaskNotFoundError(task_id)

    def save(self, task: Task) -> None:
        """Save a task."""
        tasks = self._load_tasks()

        # Update existing task or append new one
        updated = False
        for i, task_data in enumerate(tasks):
            if UUID(task_data["id"]) == task.id:
                tasks[i] = self._task_to_dict(task)
                updated = True
                break

        if not updated:
            tasks.append(self._task_to_dict(task))

        self._save_tasks(tasks)

    def delete(self, task_id: UUID) -> None:
        """Delete a task."""
        tasks = self._load_tasks()
        tasks = [t for t in tasks if UUID(t["id"]) != task_id]
        self._save_tasks(tasks)

    def find_by_project(self, project_id: UUID) -> Sequence[Task]:
        """Find all tasks for a project."""
        tasks = self._load_tasks()
        return [self._dict_to_task(t) for t in tasks if UUID(t["project_id"]) == project_id]

    def get_active_tasks(self) -> Sequence[Task]:
        """Get all non-completed tasks."""
        tasks = self._load_tasks()
        return [self._dict_to_task(t) for t in tasks if t["status"] != TaskStatus.DONE.name]


class FileProjectRepository(ProjectRepository):
    """JSON file-based implementation of ProjectRepository."""

    def __init__(self, data_dir: Path):
        self.projects_file = data_dir / "projects.json"
        self._ensure_file_exists()

        # Create the task repository
        self.task_repository = FileTaskRepository(data_dir)

        """
        Initialize INBOX if doesn't exist
        The key is that while INBOX's existence is guaranteed by 
        infrastructure, its behavior and rules remain in the domain layer.
        """
        inbox = self._fetch_inbox()
        if not inbox:
            inbox = Project.create_inbox()
            self.save(inbox)

    def _ensure_file_exists(self) -> None:
        """Create the projects file if it doesn't exist."""
        if not self.projects_file.exists():
            self.projects_file.write_text("[]")

    def _load_projects(self) -> list[Dict[str, Any]]:
        """Load all projects from the JSON file."""
        return json.loads(self.projects_file.read_text())

    def _save_projects(self, projects: list[Dict[str, Any]]) -> None:
        """Save projects to the JSON file."""
        self.projects_file.write_text(json.dumps(projects, indent=2, cls=JsonEncoder))

    def _project_to_dict(self, project: Project) -> Dict[str, Any]:
        """Convert a Project entity to a dictionary for JSON storage."""
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "project_type": project.project_type.name,
            "status": project.status.name,
            "completed_at": project.completed_at,
            "completion_notes": project.completion_notes,
        }

    def _dict_to_project(self, data: Dict[str, Any]) -> Project:
        """Convert a dictionary to a Project entity."""
        # Handle INBOX project specially
        if data.get("project_type") == ProjectType.INBOX.name:
            project = Project.create_inbox()
        else:
            project = Project(name=data["name"], description=data["description"])

        # Set additional attributes
        project.status = ProjectStatus[data["status"]]
        if data["completed_at"]:
            project.completed_at = datetime.fromisoformat(data["completed_at"])
        project.completion_notes = data["completion_notes"]

        # Explicitly set ID to maintain consistency
        project.id = UUID(data["id"])

        # Load associated tasks
        self._load_project_tasks(project)

        return project

    def get(self, project_id: UUID) -> Project:
        """Retrieve a project by ID."""
        projects = self._load_projects()
        for project_data in projects:
            if UUID(project_data["id"]) == project_id:
                return self._dict_to_project(project_data)
        raise ProjectNotFoundError(project_id)

    def get_all(self) -> List[Project]:
        """Get all projects with their tasks loaded."""
        projects = [self._dict_to_project(p) for p in self._load_projects()]
        return projects

    def save(self, project: Project) -> None:
        """Save a project and its tasks."""
        projects = self._load_projects()

        # Update existing project or append new one
        updated = False
        for i, project_data in enumerate(projects):
            if UUID(project_data["id"]) == project.id:
                projects[i] = self._project_to_dict(project)
                updated = True
                break

        if not updated:
            projects.append(self._project_to_dict(project))

        self._save_projects(projects)

        # Save associated tasks
        for task in project.tasks:
            self.task_repository.save(task)

    def delete(self, project_id: UUID) -> None:
        """Delete a project and its tasks."""
        # Delete associated tasks first
        for task in self.task_repository.find_by_project(project_id):
            self.task_repository.delete(task.id)

        # Then delete the project
        projects = self._load_projects()
        projects = [p for p in projects if UUID(p["id"]) != project_id]
        self._save_projects(projects)

    def _fetch_inbox(self) -> Optional[Project]:
        """Find the INBOX project."""
        projects = self._load_projects()
        for project_data in projects:
            if project_data.get("project_type") == ProjectType.INBOX.name:
                return self._dict_to_project(project_data)
        return None

    def get_inbox(self) -> Project:
        """Get the INBOX project."""
        inbox = self._fetch_inbox()
        if not inbox:
            raise InboxNotFoundError("The Inbox project was not found")
        return inbox

    def _load_project_tasks(self, project: Project) -> None:
        """Load tasks for a project."""
        try:
            # Clear existing tasks
            project._tasks.clear()

            # Load tasks from task repository
            tasks = self.task_repository.find_by_project(project.id)

            # Associate tasks with project
            for task in tasks:
                project._tasks[task.id] = task
        except Exception as e:
            # Log error but don't crash - empty task list is better than no project
            print(f"Error loading tasks for project {project.id}: {str(e)}")
