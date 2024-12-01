"""
This module contains domain-specific exceptions for the todo application.
These exceptions represent error conditions specific to the domain model.
"""

from uuid import UUID


class DomainError(Exception):
    """Base class for domain-specific errors."""

    pass


class TaskNotFoundError(DomainError):
    """Raised when attempting to access a task that doesn't exist."""

    def __init__(self, task_id: UUID) -> None:
        self.task_id = task_id
        super().__init__(f"Task with id {task_id} not found")


class ProjectNotFoundError(DomainError):
    """Raised when attempting to access a project that doesn't exist."""

    def __init__(self, project_id: UUID) -> None:
        self.project_id = project_id
        super().__init__(f"Project with id {project_id} not found")


class InboxNotFoundError(DomainError):
    """Raised when attempting to access the INBOX project that doesn't exist."""

    pass


class ValidationError(DomainError):
    """Raised when domain validation rules are violated."""

    pass


class BusinessRuleViolation(DomainError):
    """Raised when a business rule is violated."""

    pass
