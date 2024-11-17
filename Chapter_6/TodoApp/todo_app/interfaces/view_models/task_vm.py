from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TaskViewModel:
    """View-specific representation of a task."""
    id: str
    title: str
    description: str
    status_display: str  # Human readable status
    priority_display: str  # Human readable priority
    due_date_display: Optional[str]  # Formatted date string
    project_display: Optional[str]  # Project name if available
    completion_info: Optional[str]  # Formatted completion details
