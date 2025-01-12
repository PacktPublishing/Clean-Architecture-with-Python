from dataclasses import dataclass
from uuid import UUID


@dataclass
class Task:
    """Clean Architecture: Pure domain entity."""

    title: str
    description: str
    project_id: UUID
    priority: Priority = Priority.MEDIUM


def test_new_task_priority():
    """Clean test focused purely on domain logic."""
    task = Task(
        title="Test task",
        description="Test description",
        project_id=UUID("12345678-1234-5678-1234-567812345678"),
    )
    assert task.priority == Priority.MEDIUM
