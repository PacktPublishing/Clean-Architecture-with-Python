from uuid import UUID

from todo_app.application.ports.notifications import (
    NotificationPort,
)


class ModernNotificationService:
    """Third-party service with a different interface"""

    def send_notification(self, payload: dict) -> None:
        # Modern service implementation
        pass


class ModernNotificationAdapter(NotificationPort):
    """Adapts modern notification service to work with our interface"""

    def __init__(self, modern_service: ModernNotificationService):
        self._service = modern_service

    def notify_task_completed(self, task_id: UUID) -> None:
        self._service.send_notification(
            {"type": "TASK_COMPLETED", "taskId": str(task_id)}
        )
