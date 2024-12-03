from datetime import datetime, timezone
from typing import Optional
from todo_app.domain.value_objects import Priority, TaskStatus
from todo_app.interfaces.view_models.base import ErrorViewModel
from todo_app.application.dtos.project_dtos import CompleteProjectResponse, ProjectResponse
from todo_app.interfaces.view_models.project_vm import ProjectCompletionViewModel, ProjectViewModel
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
            status_display=f"[{task_response.status.value}]",
            priority_display=self._format_priority(task_response.priority),
            due_date_display=self._format_due_date(task_response.due_date),
            project_display=(
                f"Project: {task_response.project_id}" if task_response.project_id else ""
            ),
            completion_info=self._format_completion_info(
                task_response.completion_date, task_response.completion_notes
            ),
        )

    def _format_due_date(self, due_date: Optional[datetime]) -> str:
        """Format due date, indicating if task is overdue."""
        if not due_date:
            return "No due date"

        is_overdue = due_date < datetime.now(timezone.utc)
        date_str = due_date.strftime("%Y-%m-%d")
        return f"OVERDUE - Due: {date_str}" if is_overdue else f"Due: {date_str}"

    def _format_completion_info(
        self, completion_date: Optional[datetime], completion_notes: Optional[str]
    ) -> str:
        """Format completion information including notes if present."""
        if not completion_date:
            return "Not completed"

        base_info = f"Completed on {completion_date.strftime('%Y-%m-%d %H:%M')}"
        if completion_notes:
            return f"{base_info} - {completion_notes}"
        return base_info

    def _format_priority(self, priority: Priority) -> str:
        """Format priority for CLI display."""
        display_map = {
            Priority.LOW: "Minor",
            Priority.MEDIUM: "Normal",
            Priority.HIGH: "High",
        }
        return display_map[priority]

    def present_error(self, error_msg: str, code: Optional[str] = None) -> ErrorViewModel:
        return ErrorViewModel(message=error_msg, code=code)


class CliProjectPresenter(ProjectPresenter):
    """CLI-specific project presenter."""

    def __init__(self):
        self.task_presenter = CliTaskPresenter()

    def present_project(self, project_response: ProjectResponse) -> ProjectViewModel:
        """Format project for CLI display."""
        # Convert tasks to view models
        task_vms = [self.task_presenter.present_task(task) for task in project_response.tasks]

        # Count completed tasks
        completed = sum(1 for task in project_response.tasks if task.status == TaskStatus.DONE)

        return ProjectViewModel(
            id=str(project_response.id),
            name=project_response.name,
            description=project_response.description,
            status_display=f"[{project_response.status.name}]",
            task_count=len(project_response.tasks),
            completed_task_count=completed,
            completion_info=self._format_completion_info(project_response.completion_date),
            tasks=task_vms,  # Include task view models in project view model
        )

    def present_completion(
        self, completion_response: CompleteProjectResponse
    ) -> ProjectCompletionViewModel:
        """Format project completion for CLI display."""
        return ProjectCompletionViewModel(
            project_id=str(completion_response.id),
            completion_notes=completion_response.completion_notes,
        )

    def present_error(self, error_msg: str, code: Optional[str] = None) -> ErrorViewModel:
        return ErrorViewModel(message=error_msg, code=code)

    def _format_completion_info(self, completion_date: Optional[datetime]) -> str:
        """Format completion information for CLI display."""
        if completion_date:
            return f"Completed on {completion_date.strftime('%Y-%m-%d %H:%M')}"
        return "Not completed"
