from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from uuid import UUID

from todo_app.domain.value_objects import Priority, TaskStatus
from todo_app.interfaces.view_models.project_vm import ProjectViewModel
from todo_app.interfaces.view_models.task_vm import TaskViewModel


@dataclass
class TaskReference:
    """Reference to a task using project number and task letter."""
    project_num: int
    task_letter: str
    task_id: UUID

    @property
    def reference(self) -> str:
        """Get the reference string (e.g., '1.a')."""
        return f"{self.project_num}.{self.task_letter}"


@dataclass
class ProjectReference:
    """Reference to a project using project number."""
    project_num: int
    project_id: UUID

    @property
    def reference(self) -> str:
        """Get the reference string (e.g., '1')."""
        return str(self.project_num)


class ReferenceManager:
    """Manages references between display IDs and actual IDs."""
    
    def __init__(self):
        self._task_refs: Dict[str, TaskReference] = {}
        self._project_refs: Dict[str, ProjectReference] = {}
        
    def clear(self) -> None:
        """Clear all references."""
        self._task_refs.clear()
        self._project_refs.clear()
        
    def add_project(self, num: int, project_id: UUID) -> None:
        """Add a project reference."""
        ref = ProjectReference(num, project_id)
        self._project_refs[ref.reference] = ref
        
    def add_task(self, project_num: int, letter: str, task_id: UUID) -> None:
        """Add a task reference."""
        ref = TaskReference(project_num, letter, task_id)
        self._task_refs[ref.reference] = ref
        
    def get_project_id(self, ref: str) -> Optional[UUID]:
        """Get project ID from reference."""
        project_ref = self._project_refs.get(ref)
        return project_ref.project_id if project_ref else None
        
    def get_task_id(self, ref: str) -> Optional[UUID]:
        """Get task ID from reference."""
        task_ref = self._task_refs.get(ref)
        return task_ref.task_id if task_ref else None