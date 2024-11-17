# interfaces/view_models/task_vm.py
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ProjectViewModel:
    """View-specific representation of a project."""
    id: str
    name: str
    description: str
    status_display: str
    task_count: str  # e.g., "5 tasks (2 completed)"
    completion_info: Optional[str]