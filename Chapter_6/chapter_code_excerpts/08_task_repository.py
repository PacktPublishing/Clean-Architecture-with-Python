# Defined in Application layer


from abc import ABC, abstractmethod
from uuid import UUID


class TaskRepository(ABC):

    @abstractmethod
    def get(self, task_id: UUID) -> Task:
        """Retrieve a task by its ID."""

        pass


# Implemented directly in Infrastructure layer


class SqliteTaskRepository(TaskRepository):

    def get(self, task_id: UUID) -> Task:

        # Direct implementation of interface

        pass
