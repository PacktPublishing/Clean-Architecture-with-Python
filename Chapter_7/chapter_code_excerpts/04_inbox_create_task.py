def _create_task(self) -> None:
    """Handle task creation command."""
    title = click.prompt("Task title", type=str)
    description = click.prompt("Description", type=str)

    # Project selection is optional - defaults to Inbox
    if click.confirm("Assign to a specific project?", default=False):
        project_id = self._select_project()

    # Inbox handling in use case
    result = self.app.task_controller.handle_create(
        title=title, description=description, project_id=project_id
    )
