from uuid import UUID

from todo_app.application.repositories.task_repository import (
    TaskRepository,
)
from todo_app.domain.entities.task import Task
from todo_app.domain.exceptions import TaskNotFoundError


class MongoClient:
    def __init__(self):
        self.task_management = None

    """Stub class to make mypy happy"""

    ...


class MongoDbTaskRepository(TaskRepository):
    """MongoDB implementation of the TaskRepository interface"""

    def __init__(self, client: MongoClient):
        self.client = client
        self.db = client.task_management
        self.tasks = self.db.tasks

    def get(self, task_id: UUID) -> Task:
        """Retrieve a task by its ID"""
        document = self.tasks.find_one({"_id": str(task_id)})
        if not document:
            raise TaskNotFoundError(task_id)
        # ... remainder of method implementation

    # Other interface methods implemented ...
