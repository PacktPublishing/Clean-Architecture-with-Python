# CLI Presenter from Chapter 7
def present_task(self, task_response: TaskResponse) -> TaskViewModel:
    """Format task for CLI display."""
    return TaskViewModel(
        id=task_response.id,
        title=task_response.title,
        status_display=f"[{task_response.status.value}]",  # CLI-specific bracketed format
        priority_display=self._format_priority(task_response.priority),  # CLI-specific coloring
    )
