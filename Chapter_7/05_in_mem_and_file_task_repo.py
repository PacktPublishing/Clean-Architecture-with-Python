from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict
from uuid import UUID


class TaskRepository(ABC):
    """Repository interface for Task entity persistence."""

    @abstractmethod
    def get(self, task_id: UUID) -> Task:
        """Retrieve a task by its ID."""
        pass

    @abstractmethod
    def save(self, task: Task) -> None:
        """Save a task to the repository."""
        pass

    # ... remaining methods of interface


class InMemoryTaskRepository(TaskRepository):
    """In-memory implementation of TaskRepository."""

    def __init__(self) -> None:
        self._tasks: Dict[UUID, Task] = {}

    def get(self, task_id: UUID) -> Task:
        """Retrieve a task by ID."""
        if task := self._tasks.get(task_id):
            return task
        raise TaskNotFoundError(task_id)

    def save(self, task: Task) -> None:
        """Save a task."""
        self._tasks[task.id] = task

    # additional interface method implementations


class FileTaskRepository(TaskRepository):
    """JSON file-based implementation of TaskRepository."""

    def __init__(self, data_dir: Path):
        self.tasks_file = data_dir / "tasks.json"
        self._ensure_file_exists()

    def get(self, task_id: UUID) -> Task:
        """Retrieve a task by ID."""
        tasks = self._load_tasks()
        for task_data in tasks:
            if UUID(task_data["id"]) == task_id:
                return self._dict_to_task(task_data)
        raise TaskNotFoundError(task_id)

    def save(self, task: Task) -> None:
        """Save a task."""
        # ... remainder of implementation


# Works identically with either repository
task = repository.get(task_id)
task.complete()
repository.save(task)
