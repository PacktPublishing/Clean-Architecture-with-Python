# In the Domain layer (e.g., todo_app/domain/repositories/task_repository.py)
from abc import ABC, abstractmethod

from todo_app.domain.entities.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def save(self, task: Task):
        pass

    @abstractmethod
    def get(self, task_id: str) -> Task:
        pass


# In the Domain layer (e.g., todo_app/domain/services/task_service.py)
class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def create_task(self, title: str, description: str) -> Task:
        task = Task(title, description)
        self.task_repository.save(task)
        return task

    def mark_task_as_complete(self, task_id: str) -> Task:
        task = self.task_repository.get(task_id)
        task.complete()
        self.task_repository.save(task)
        return task


# In an outer layer
# (e.g., todo_app/infrastructure/persistence/sqlite_task_repository.py)
class SQLiteTaskRepository(TaskRepository):
    def __init__(self, db_connection):
        self.db = db_connection

    def save(self, task: Task):
        # Implementation details...
        pass

    def get(self, task_id: str) -> Task:
        # Implementation details...
        pass
