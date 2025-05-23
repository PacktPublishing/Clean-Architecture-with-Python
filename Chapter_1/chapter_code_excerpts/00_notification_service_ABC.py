from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send_notification(self, message: str) -> None:
        pass


class EmailNotifier(Notifier):
    def send_notification(self, message: str) -> None:

        print(f"Sending email: {message}")


class SMSNotifier(Notifier):
    def send_notification(self, message: str) -> None:

        print(f"Sending SMS: {message}")


class NotificationService:
    def __init__(self, notifier: Notifier):

        self.notifier = notifier

    def notify(self, message: str) -> None:
        self.notifier.send_notification(message)


# Usage
email_notifier = EmailNotifier()
email_service = NotificationService(email_notifier)
email_service.notify("Hello via email")
