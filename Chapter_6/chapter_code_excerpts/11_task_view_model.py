from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TaskViewModel:
    """View-specific representation of a task."""

    id: str
    title: str
    description: str
    status_display: str  # Pre-formatted for display
    priority_display: str  # Pre-formatted for display
    due_date_display: Optional[str]  # Pre-formatted for display
    project_display: Optional[str]  # Pre-formatted project context
    completion_info: Optional[str]  # Pre-formatted completion details
