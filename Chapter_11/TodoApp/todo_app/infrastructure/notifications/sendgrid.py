# todo_app/infrastructure/notifications/sendgrid.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging

from todo_app.application.service_ports.notifications import NotificationPort
from todo_app.domain.entities.task import Task
from todo_app.infrastructure.config import Config

logger = logging.getLogger(__name__)


class SendGridNotifier(NotificationPort):
    """SendGrid implementation of notification port."""

    def __init__(self) -> None:
        self.api_key = Config.get_sendgrid_api_key()
        self.notification_email = Config.get_notification_email()
        self._init_sg_client()

    def _init_sg_client(self):
        if not self.api_key:
            logger.error("SendGrid API key not found, skipping client initialization")
            raise ValueError("SendGrid API key not found")
        self.client = SendGridAPIClient(self.api_key)

    def notify_task_completed(self, task: Task) -> None:
        """Send email notification for completed task if configured."""
        if not (self.client and self.notification_email):
            logger.warning(
                f"SendGrid not configured, skipping notification, task_id: {str(task.id)}"
            )
            return
        obfuscated_key = f"{self.api_key[:4]}...{self.api_key[-4:]}" if self.api_key else "None"
        logger.info(
            f"Attempting to send notification with SendGrid - "
            f"API Key: {obfuscated_key}, "
            f"Email: {self.notification_email}"
        )
        try:
            message = Mail(
                from_email=self.notification_email,
                to_emails=self.notification_email,
                subject=f"Task Completed: {task.title}",
                html_content=f"<strong>Task '{task.title}'</strong> has been completed.",
            )
            response = self.client.send(message)
            logger.info(
                f"Notification sent successfully - task_id: {str(task.id)}, "
                f"notification_email: {self.notification_email}, "
                f"response: {response.status_code}"
            )
        except Exception as e:
            # Log error but don't disrupt business operations
            logger.error(
                f"Failed to send completion notification for task {str(task.id)}: {str(e)}"
            )

    def notify_task_high_priority(self, task: Task) -> None:
        """Not implemented - using NotificationPort interface."""
        pass

    def notify_task_deadline_approaching(self, task: Task, days_remaining: int) -> None:
        """Not implemented - using NotificationPort interface."""
        pass
