"""
Base implementation for interactive CLI interface.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
from uuid import UUID

from todo_app.infrastructure.configuration.container import Application
from todo_app.infrastructure.cli.components.references import ReferenceManager
from todo_app.infrastructure.cli.components.display import CliDisplay

from todo_app.domain.value_objects import Priority, TaskStatus


class BaseInteractiveCli(ABC):
    """Base class for interactive CLI implementations."""

    def __init__(self, app: Application):
        self.app = app
        self.refs = ReferenceManager()
        self.display = CliDisplay()

    def run(self) -> int:
        """Run the interactive CLI interface."""
        while True:
            try:
                # Display projects and tasks
                projects = self._fetch_projects()
                print(self.display.format_projects_and_tasks(projects, self.refs))
                print("\nSelect a project or task to work with")
                print("Example: 1.a for task or just 1 for project")

                # Get user selection
                selection = self._get_input("? ")
                if not selection:
                    return 0

                # Handle selection
                if "." in selection:
                    # Task selection
                    task_id = self.refs.get_task_id(selection)
                    if task_id:
                        self._handle_task(task_id)
                    else:
                        print(f"Invalid task reference: {selection}")
                else:
                    # Project selection
                    project_id = self.refs.get_project_id(selection)
                    if project_id:
                        self._handle_project(project_id)
                    else:
                        print(f"Invalid project reference: {selection}")

            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                continue
            except EOFError:
                print("\nExiting...")
                return 0
            except Exception as e:
                print(f"Error: {str(e)}")
                return 1

    def _handle_task(self, task_id: UUID) -> None:
        """Handle task-related actions."""
        result = self._get_task(task_id)
        if not result.is_success:
            print(result.error.message)
            return

        # Display task details
        task = result.success
        print("\n" + self.display.format_task_detail(task))

        # Show and handle actions
        actions_text, actions = self.display.format_task_actions()
        print(actions_text)

        action = self._get_input("")
        if not action:
            return

        if action not in actions:
            print(f"Invalid action: {action}")
            return

        self._handle_task_action(task_id, action)

    def _handle_task_action(self, task_id: UUID, action: str) -> None:
        """Handle specific task action."""
        if action == "1":  # Edit status
            options = self.display.format_status_options()
            self._show_options("Select status:", options)
            choice = self._get_input("? ")
            if choice in options:
                self._update_task_status(task_id, options[choice])

        elif action == "2":  # Edit priority
            options = self.display.format_priority_options()
            self._show_options("Select priority:", options)
            choice = self._get_input("? ")
            if choice in options:
                self._update_task_priority(task_id, options[choice])

        # ... Additional actions to be implemented

    @abstractmethod
    def _get_input(self, prompt: str) -> str:
        """Get input from user."""
        pass

    @abstractmethod
    def _show_options(self, title: str, options: dict) -> None:
        """Show options to user."""
        pass

    @abstractmethod
    def _fetch_projects(self) -> list:
        """Fetch projects from application."""
        pass

    @abstractmethod
    def _get_task(self, task_id: UUID) -> Any:
        """Get task details."""
        pass

    @abstractmethod
    def _update_task_status(self, task_id: UUID, status: TaskStatus) -> None:
        """Update task status."""
        pass

    @abstractmethod
    def _update_task_priority(self, task_id: UUID, priority: Priority) -> None:
        """Update task priority."""
        pass

    @abstractmethod
    def _handle_project(self, project_id: UUID) -> None:
        """Handle project-related actions."""
        pass
