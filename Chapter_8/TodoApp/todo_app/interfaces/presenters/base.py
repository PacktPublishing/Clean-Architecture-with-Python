from abc import ABC, abstractmethod
from typing import Optional

from todo_app.interfaces.view_models.base import ErrorViewModel
from todo_app.application.dtos.project_dtos import CompleteProjectResponse, ProjectResponse
from todo_app.application.dtos.task_dtos import TaskResponse
from todo_app.interfaces.view_models.project_vm import ProjectCompletionViewModel, ProjectViewModel
from todo_app.interfaces.view_models.task_vm import TaskViewModel

class TaskPresenter(ABC):
    """Abstract base presenter for task-related output."""
    
    @abstractmethod
    def present_task(self, task_response: TaskResponse) -> TaskViewModel:
        """Convert task response to view model."""
        pass
        
    @abstractmethod
    def present_error(self, error_msg: str, code: Optional[str] = None) -> ErrorViewModel:
        """Format error message for display."""
        pass

class ProjectPresenter(ABC):
    """Abstract base presenter for project-related output."""
    
    @abstractmethod
    def present_project(self, project_response: ProjectResponse) -> ProjectViewModel:
        """Convert project response to view model."""
        pass
        
    @abstractmethod
    def present_completion(self, completion_response: CompleteProjectResponse) -> ProjectCompletionViewModel:
        """Format project completion message."""
        pass
        
    @abstractmethod
    def present_error(self, error_msg: str, code: Optional[str] = None) -> ErrorViewModel:
        """Format error message for display."""
        pass