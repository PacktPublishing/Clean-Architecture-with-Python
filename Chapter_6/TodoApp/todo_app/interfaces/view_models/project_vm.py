from dataclasses import dataclass
from typing import Optional

from todo_app.interfaces.view_models.task_vm import TaskViewModel


@dataclass(frozen=True)
class ProjectViewModel:
    """View-specific representation of a project."""

    id: str
    name: str
    description: str
    status_display: str
    task_count: int
    completed_task_count: int
    completion_info: Optional[str]
    tasks: list[TaskViewModel]


@dataclass(frozen=True)
class ProjectCompletionViewModel:
    """View-specific representation of a project completion."""

    project_id: str
    completion_notes: Optional[str]
