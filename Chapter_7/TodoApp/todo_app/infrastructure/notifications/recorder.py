"""
Simple notification implementation for demonstrating Interface Adapters patterns.

This is a preimptive view into the Framworks and Drivers layer.

This module provides a basic implementation of the notification interface to
demonstrate Clean Architecture principles without the complexity of real
notification services. It shows:
- How notification interfaces from the Application layer are implemented
- How notification concerns are kept separate from business logic
- Basic handling of notification events

This implementation will be replaced by actual notification services in Chapter 7,
demonstrating how Clean Architecture enables swapping notification mechanisms
while maintaining core functionality.
"""

from dataclasses import dataclass
from uuid import UUID
from todo_app.application.service_ports.notifications import NotificationPort

@dataclass
class NotificationRecorder(NotificationPort):
    """
    Simple notification implementation for teaching Interface Adapters concepts.
    
    This class demonstrates how notification gateways work in Clean Architecture:
    - Implements interface defined by Application layer
    - Encapsulates notification details (simple printing in this case)
    - Maintains separation between notification and business logic
    
    While simplified, this implementation establishes patterns that will be used
    in actual notification service implementations.
    """
    
    def __init__(self) -> None:
        self.completed_tasks = []
        self.high_priority_tasks = []
        self.deadline_warnings = []

    def notify_task_completed(self, task_id: UUID) -> None:
        """Record a task completion notification."""
        message = f"Task {task_id} has been completed"
        print(f"NOTIFICATION: {message}")
        self.completed_tasks.append(task_id)

    def notify_task_high_priority(self, task_id: UUID) -> None:
        """Record a high priority task notification."""
        message = f"Task {task_id} has been set to high priority"
        print(f"NOTIFICATION: {message}")
        self.high_priority_tasks.append(task_id)

    def notify_task_deadline_approaching(
        self, task_id: UUID, days_remaining: int
    ) -> None:
        """Record a deadline approaching notification."""
        message = f"Task {task_id} deadline approaching in {days_remaining} days"
        print(f"NOTIFICATION: {message}")
        self.deadline_warnings.append((task_id, days_remaining))