from todo_app.application.service_ports.notifications import NotificationPort
from todo_app.infrastructure.notifications.recorder import NotificationRecorder
from todo_app.infrastructure.notifications.sendgrid import SendGridNotifier
from todo_app.infrastructure.config import Config

def create_notification_service() -> NotificationPort:
    """
    Create appropriate notification service based on configuration.
    Falls back to NotificationRecorder if SendGrid is not configured.
    """
    api_key = Config.get_sendgrid_api_key()
    notification_email = Config.get_notification_email()
    
    if api_key and notification_email:
        return SendGridNotifier()
    
    return NotificationRecorder()