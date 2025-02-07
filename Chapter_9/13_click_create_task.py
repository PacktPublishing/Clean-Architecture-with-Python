# todo_app/infrastructure/cli/click_cli_app.py
def _create_task(self):
    """CLI task creation."""
    title = click.prompt("Task title", type=str)
    description = click.prompt("Description", type=str)
    result = self.app.task_controller.handle_create(title=title, description=description)
