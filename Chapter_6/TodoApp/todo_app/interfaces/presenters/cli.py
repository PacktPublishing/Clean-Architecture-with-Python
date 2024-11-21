# interfaces/presenters/cli.py
from typing import Optional
from todo_app.interfaces.view_models.base import ErrorViewModel
from todo_app.application.dtos.project_dtos import CompleteProjectResponse, ProjectResponse
from todo_app.interfaces.view_models.project_vm import ProjectViewModel
from todo_app.application.dtos.task_dtos import TaskResponse
from todo_app.interfaces.presenters.base import ProjectPresenter, TaskPresenter
from todo_app.interfaces.view_models.task_vm import TaskViewModel


class CliTaskPresenter(TaskPresenter):
    """CLI-specific task presenter."""
    
    def present_task(self, task_response: TaskResponse) -> TaskViewModel:
        """Format task for CLI display."""
        return TaskViewModel(
            id=task_response.id,
            title=task_response.title,
            description=task_response.description,
            status_display=f"[{task_response.status}]",
            priority_display=f"Priority: {task_response.priority}",
            due_date_display=f"Due: {task_response.due_date}" if task_response.due_date else "No due date",
            project_display=f"Project: {task_response.project_id}" if task_response.project_id else None,
            completion_info=f"Completed: {task_response.completion_date}" if task_response.completion_date else None
        )
    
    def present_error(self, error_msg: str, code: Optional[str] = None) -> ErrorViewModel:
        return ErrorViewModel(
            message=error_msg,
            code=code
        )

class CliProjectPresenter(ProjectPresenter):
    """CLI-specific project presenter."""
    
    def present_project(self, project_response: ProjectResponse) -> ProjectViewModel:
        """Format project for CLI display."""
        return ProjectViewModel(
            id=project_response.id,
            name=project_response.name,
            description=project_response.description,
            status_display=f"[{project_response.status}]",
            task_count=str(len(project_response.tasks)),
            completion_info=f"Completed: {project_response.completion_date}" if project_response.completion_date else None
        )
    
    def present_completion(self, completion_response: CompleteProjectResponse) -> str:
        """Format project completion for CLI display."""
        return f"Project {completion_response.id} completed on {completion_response.completion_date}"
    
    def present_error(self, error_msg: str, code: Optional[str] = None) -> ErrorViewModel:
        return ErrorViewModel(
            message=error_msg,
            code=code
        )