from datetime import datetime, timezone
from typing import Optional
from todo_app.domain.value_objects import Priority
from todo_app.interfaces.view_models.base import ErrorViewModel
from todo_app.application.dtos.task_dtos import TaskResponse
from todo_app.interfaces.presenters.base import TaskPresenter
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
