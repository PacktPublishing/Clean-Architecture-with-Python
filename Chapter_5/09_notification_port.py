# Port: Defines capability needed by Application Layer
from abc import abstractmethod, ABC
from uuid import UUID


class NotificationPort(ABC):

    @abstractmethod
    def notify_task_completed(self, task: Task) -> None:
        """Notify when a task is completed"""
        pass

    # other capabilities as needed
