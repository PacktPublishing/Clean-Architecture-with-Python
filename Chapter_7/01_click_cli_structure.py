class ClickCli:
    def __init__(self, app: Application):
        self.app = app
        self.current_projects = []  # Cached list of projects for display

    def run(self) -> int:
        """Entry point for running the Click CLI application"""
        try:
            while True:
                self._display_projects()
                self._handle_selection()
        except KeyboardInterrupt:
            click.echo("\nGoodbye!", err=True)
            return 0

    def _display_task_menu(self, task_id: str) -> None:
        """Display and handle task menu."""
        result = self.app.task_controller.handle_get(task_id)
        if not result.is_success:
            click.secho(result.error.message, fg="red", err=True)
            return
        task = result.success
        click.clear()
        click.echo("\nTASK DETAILS")
        click.echo("=" * 40)
        click.echo(f"Title:       {task.title}")
        click.echo(f"Description: {task.description}")
        click.echo(f"Status:      {task.status_display}")
        click.echo(f"Priority:    {task.priority_display}")

    def _handle_selection(self) -> None:
        """Handle project/task selection."""
        selection = (
            click.prompt(
                "\nSelect a project or task (e.g., '1' or '1.a')", type=str, show_default=False
            )
            .strip()
            .lower()
        )
        if selection == "np":
            self._create_new_project()
            return
        try:
            if "." in selection:
                project_num, task_letter = selection.split(".")
                self._handle_task_selection(int(project_num), task_letter)
            else:  # Project selection
                self._handle_project_selection(int(selection))
        except (ValueError, IndexError):
            click.secho(
                "Invalid selection. Use '1' for project or '1.a' for task.",
                fg="red",
                err=True,
            )

    def _create_new_project(self) -> None:
        """Create a new project."""
        name = click.prompt("Project name", type=str)
        description = click.prompt("Description (optional)", type=str, default="")
        result = self.app.project_controller.handle_create(name, description)
        if not result.is_success:
            click.secho(result.error.message, fg="red", err=True)

    # ... additional methods
