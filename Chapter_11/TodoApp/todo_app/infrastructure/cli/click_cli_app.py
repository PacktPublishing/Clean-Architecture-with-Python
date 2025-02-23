"""
Enhanced Click-based CLI implementation with project actions.
"""

from typing import Optional
import click

from todo_app.interfaces.view_models.task_vm import TaskViewModel
from todo_app.interfaces.view_models.project_vm import ProjectViewModel
from todo_app.infrastructure.configuration.container import Application
from todo_app.domain.value_objects import Priority
from todo_app.infrastructure.logging.trace import set_trace_id, get_trace_id


class ClickCli:
    def __init__(self, app: Application):
        self.app = app
        self.current_projects = []  # Cached list of projects for display

    def run(self) -> int:
        """Entry point for running the Click CLI application"""
        try:
            # Set trace ID for CLI session
            set_trace_id()

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

    def _handle_project_menu(self, project: ProjectViewModel) -> None:
        """Handle project menu actions."""
        while True:
            # Get latest project data
            result = self.app.project_controller.handle_get(project.id)
            if not result.is_success:
                click.secho(result.error.message, fg="red", err=True)
                return
            project = result.success

            click.clear()
            click.echo(f"\nProject: {project.name}")
            click.echo(f"Status: {project.status_display}")
            click.echo(f"Description: {project.description}")
            click.echo(
                f"\nTasks: {project.task_count} total, {project.completed_task_count} completed"
            )

            click.echo("\nActions:")
            # Only show edit option for non-INBOX projects
            if project.project_type != "INBOX":
                click.echo("[1] Edit Project")
                click.echo("[2] Add Task to Project")
                click.echo("[3] Return to main menu")
            else:
                click.echo("[1] Add Task to Project")
                click.echo("[2] Return to main menu")

            if project.project_type != "INBOX":
                choice = click.prompt("Select an action", type=str, default="3")
                if choice == "1":
                    self._edit_project(project)
                elif choice == "2":
                    self._add_task_to_project(project)
                elif choice == "3":
                    break
            else:
                choice = click.prompt("Select an action", type=str, default="2")
                if choice == "1":
                    self._add_task_to_project(project)
                elif choice == "2":
                    break

    def _create_task(self, project_id: str) -> Optional[TaskViewModel]:
        """Create a new task."""
        click.echo("\nAdd New Task")
        title = click.prompt("Task title", type=str)
        description = click.prompt("Description", type=str, default="")
        priority = self._get_task_priority()

        # Create the task
        result = self.app.task_controller.handle_create(
            title=title,
            description=description,
            project_id=project_id,
            priority=priority,
        )

        if not result.is_success:
            click.secho(result.error.message, fg="red", err=True)
            return

        click.echo("Task created successfully!")
        return result.success

    def _add_task_to_project(self, project: ProjectViewModel) -> None:
        """Add a new task to the project."""
        task = self._create_task(project.id)
        if task:
            # Refresh projects list
            refresh_result = self.app.project_controller.handle_list()
            if refresh_result.is_success:
                self.current_projects = refresh_result.success
        click.pause()

    def _get_task_priority(self) -> str:
        """Get task priority from user input."""
        click.echo("\nPriority:")
        click.echo("[1] Low")
        click.echo("[2] Medium")
        click.echo("[3] High")
        priority_choice = click.prompt("Select priority", type=str, default="2")

        priority_map = {"1": "LOW", "2": "MEDIUM", "3": "HIGH"}
        return priority_map.get(priority_choice, "MEDIUM")

    def _edit_project(self, project: ProjectViewModel) -> None:
        """Edit project details."""
        click.echo("\nEdit Project")
        click.echo("Leave blank to keep current value")

        current_name = project.name
        current_description = project.description

        # Show current values and get new ones
        click.echo(f"\nCurrent name: {current_name}")
        new_name = click.prompt("New name", type=str, default="", show_default=False)

        click.echo(f"\nCurrent description: {current_description}")
        new_description = click.prompt("New description", type=str, default="", show_default=False)

        # Only update if new values were provided
        result = self.app.project_controller.handle_update(
            project_id=project.id,
            name=new_name if new_name else None,
            description=new_description if new_description else None,
        )

        if result.is_success:
            click.echo("Project updated successfully!")
        else:
            click.secho(result.error.message, fg="red", err=True)

        click.pause()

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
        self._handle_project_menu(project)

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

    def _create_new_project(self) -> None:
        """Create a new project."""
        name = click.prompt("Project name", type=str)
        description = click.prompt("Description (optional)", type=str, default="")

        result = self.app.project_controller.handle_create(name, description)
        if not result.is_success:
            click.secho(result.error.message, fg="red", err=True)

    def _display_task_menu(self, task_id: str) -> None:
        """Display and handle task menu."""
        while True:
            result = self.app.task_controller.handle_get(task_id)
            if not result.is_success:
                click.secho(result.error.message, fg="red", err=True)
                return

            task = result.success
            click.clear()
            # Display task details in a clear format
            click.echo("\nTASK DETAILS")
            click.echo("=" * 40)
            click.echo(f"Title:       {task.title}")
            click.echo(f"Description: {task.description}")
            click.echo(f"Status:      {task.status_display}")
            click.echo(f"Priority:    {task.priority_display}")
            if task.completion_info:
                click.echo(f"Completion:  {task.completion_info}")
            click.echo("=" * 40)

            # Display simplified action menu
            click.echo("\nActions:")
            click.echo("[1] Edit title")
            click.echo("[2] Edit description")
            click.echo("[3] Edit priority")
            click.echo("[4] Complete task")
            click.echo("[5] Delete task")
            click.echo("[Enter] Return to main menu")

            choice = click.prompt("Choose an action", type=str, default="")

            if choice == "1":  # Edit title
                new_title = click.prompt("New title", type=str)
                result = self.app.task_controller.handle_update(task_id, title=new_title)
                if not result.is_success:
                    click.secho(result.error.message, fg="red", err=True)
                    click.pause()
            elif choice == "2":  # Edit description
                new_description = click.prompt("New description", type=str)
                result = self.app.task_controller.handle_update(
                    task_id, description=new_description
                )
                if not result.is_success:
                    click.secho(result.error.message, fg="red", err=True)
                    click.pause()
            elif choice == "3":  # Edit priority
                self._update_task_priority(task_id)
                break
            elif choice == "4":  # Complete task
                self._complete_task(task_id)
            elif choice == "5":  # Delete task
                if click.confirm("Are you sure you want to delete this task?"):
                    result = self.app.task_controller.handle_delete(task_id)
                    if result.is_success:
                        click.echo("Task deleted successfully")
                        break
                    else:
                        click.secho(result.error.message, fg="red", err=True)
                        click.pause()
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
            result = self.app.task_controller.handle_update(
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
