class WebTaskPresenter(TaskPresenter):

    def present_task(self, task_response: TaskResponse) -> TaskViewModel:
        """Format task for web display."""
        return TaskViewModel(
            id=task_response.id,
            title=task_response.title,
            description=task_response.description,
            status_display=task_response.status.value,
            priority_display=task_response.priority.name,
            due_date_display=self._format_due_date(task_response.due_date),
            project_display=task_response.project_id,
            completion_info=self._format_completion_info(
                task_response.completion_date, task_response.completion_notes
            ),
        )
