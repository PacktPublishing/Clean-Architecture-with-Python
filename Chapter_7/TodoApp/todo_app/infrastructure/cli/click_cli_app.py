"""
Click-based CLI implementation.
"""

from uuid import UUID
import click

from todo_app.infrastructure.configuration.container import Application
from todo_app.domain.value_objects import Priority


class ClickCli:
    def __init__(self, app: Application):
        self.app = app
        self.current_projects = []  # Track current projects for selection

    def run(self) -> int:
        """Entry point for running the Click CLI application"""
        try:
            while True:
                self._display_projects()
                self._handle_selection()
        except KeyboardInterrupt:
            click.echo("\nGoodbye!", err=True)
            return 0

    def _display_projects(self) -> None:
        """Display all projects and their tasks."""
        click.clear()
        click.echo("\nProjects: [type 'np' to create new project]")

        result = self.app.project_controller.handle_list()
        if not result.is_success:
            click.secho(result.error.message, fg="red", err=True)
            return

        self.current_projects = result.success
        for i, project in enumerate(self.current_projects, 1):
            click.echo(f"[{i}] Project: {project.name}")
            for j, task in enumerate(project.tasks):
                task_letter = chr(97 + j)
                click.echo(
                    f"  [{task_letter}] {task.title} {task.status_display} {task.priority_display}"
                )

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
            if "." in selection:  # Task selection (e.g., "1.a")
                project_num, task_letter = selection.split(".")
                self._handle_task_selection(int(project_num), task_letter)
            else:  # Project selection
                self._handle_project_selection(int(selection))
        except (ValueError, IndexError):
            click.secho(
                "Invalid selection format. Use '1' for project or '1.a' for task.",
                fg="red",
                err=True,
            )

    def _handle_project_selection(self, project_num: int) -> None:
        """Handle project selection."""
        if not 1 <= project_num <= len(self.current_projects):
            click.secho("Invalid project number.", fg="red", err=True)
            return

        project = self.current_projects[project_num - 1]
        click.echo(f"\nProject: {project.name}")
        click.echo(f"Status: {project.status_display}")
        click.echo(f"Description: {project.description}")
        # Add project actions if needed
        click.pause()

    def _handle_task_selection(self, project_num: int, task_letter: str) -> None:
        """Handle task selection."""
        if not 1 <= project_num <= len(self.current_projects):
            click.secho("Invalid project number.", fg="red", err=True)
            return

        project = self.current_projects[project_num - 1]
        task_index = ord(task_letter) - ord("a")

        if not 0 <= task_index < len(project.tasks):
            click.secho("Invalid task letter.", fg="red", err=True)
            return

        task = project.tasks[task_index]
        self._display_task_menu(task.id)

    def _display_task_menu(self, task_id: str) -> None:
        """Display and handle task menu."""
        while True:
            task = self.app.task_repository.get(UUID(task_id))
            click.clear()
            click.echo(f"\nTask: {task.title}")
            click.echo(f"Status: [{task.status.name}]")
            click.echo(f"Priority: [{task.priority.name}]")
            if task.due_date:
                click.echo(f"Due Date: {task.due_date.due_date.strftime('%Y-%m-%d')}")
            click.echo(f"Description: {task.description}")

            # Display task actions
            actions = {
                "1": "Edit status",
                "2": "Edit priority",
                "3": "Edit due date",
                "4": "Edit description",
                "5": "Move to project",
                "6": "Complete task",
                "7": "Delete task",
            }

            click.echo("\nActions:")
            for key, action in actions.items():
                click.echo(f"[{key}] {action}")

            choice = click.prompt("Choose an action", type=str, show_default=False)

            if choice == "2":  # Edit priority
                self._update_task_priority(task_id)
            elif choice == "6":  # Complete task
                self._complete_task(task_id)
                break
            elif choice == "":  # Return to project list
                break

    def _update_task_priority(self, task_id: str) -> None:
        """Update task priority."""
        priorities = {"1": Priority.LOW, "2": Priority.MEDIUM, "3": Priority.HIGH}

        click.echo("\nPriorities:")
        for key, priority in priorities.items():
            click.echo(f"[{key}] {priority.name}")

        choice = click.prompt("Select priority", type=str)
        if choice in priorities:
            result = self.app.task_controller.handle_set_priority(
                task_id=str(task_id), priority=priorities[choice].name
            )
            if not result.is_success:
                click.secho(result.error.message, fg="red", err=True)

    def _complete_task(self, task_id: str) -> None:
        """Complete a task."""
        notes = click.prompt("Completion notes (optional)", type=str, default="")
        result = self.app.task_controller.handle_complete(
            task_id=str(task_id), notes=notes if notes else None
        )
        if not result.is_success:
            click.secho(result.error.message, fg="red", err=True)

    def _create_new_project(self) -> None:
        name = click.prompt("Project name", type=str)
        description = click.prompt("Description (optional)", type=str, default="")

        result = self.app.project_controller.handle_create(name, description)
        if not result.is_success:
            click.secho(result.error.message, fg="red", err=True)
