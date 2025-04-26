from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
class NotificationPort(ABC): 
    """Interface for sending notifications about task events.""" 
     
    @abstractmethod 
    def notify_task_completed(self, task: Task) -> None: 
        """Notify when a task is completed.""" 
        pass 
 
    @abstractmethod 
    def notify_task_high_priority(self, task: Task) -> None: 
        """Notify when a task is set to high priority.""" 
        pass
class Config: 
    """Application configuration.""" 
    # Previous repository settings omitted... 
     
    @classmethod 
    def get_sendgrid_api_key(cls) -> str: 
        """Get the SendGrid API key.""" 
        return os.getenv("TODO_SENDGRID_API_KEY", "") 
 
    @classmethod 
    def get_notification_email(cls) -> str: 
        """Get the notification recipient email.""" 
        return os.getenv("TODO_NOTIFICATION_EMAIL", "") 
    # ... remainder of implementation
    
class SendGridNotifier(NotificationPort): 
 
    def __init__(self) -> None: 
        self.api_key = Config.get_sendgrid_api_key() 
        self.notification_email = Config.get_notification_email() 
        self._init_sg_client() 
 
    def notify_task_completed(self, task: Task) -> None: 
        """Send email notification for completed task if configured.""" 
        if not (self.client and self.notification_email): 
            return   
        try: 
            message = Mail( 
                from_email=self.notification_email, 
                to_emails=self.notification_email, 
                subject=f"Task Completed: {task.title}", 
                plain_text_content=f"Task '{task.title}' has been completed." 
            ) 
            self.client.send(message) 
        except Exception as e: 
            # Log error but don't disrupt business operations 
            # ...

# Let's see how this fits into our task completion workflow. Recall from 
# Chapter 5 our CompleteTaskUseCase that coordinates task completion with notifications: 
@dataclass 
class CompleteTaskUseCase: 
    task_repository: TaskRepository 
    notification_service: NotificationPort    
 
    def execute(self, request: CompleteTaskRequest) -> Result: 
        try: 
            task = self.task_repository.get(request.task_id) 
            task.complete(notes=request.completion_notes) 
            self.task_repository.save(task) 
            self.notification_service.notify_task_completed(task) 
            # ... remainder of implementation

        except :
            ... 