from typing import Dict, Tuple
from uuid import UUID

from todo_app.interfaces.view_models.task_vm import TaskViewModel
from todo_app.infrastructure.cli.components.references import ReferenceManager
from todo_app.interfaces.view_models.project_vm import ProjectViewModel
from todo_app.domain.value_objects import Priority, TaskStatus


class CliDisplay:
    """Handles display formatting for the CLI."""

    @staticmethod
    def format_projects_and_tasks(projects: list[ProjectViewModel], refs: ReferenceManager) -> str:
        """Format projects and tasks for display."""
        refs.clear()
        lines = ["Projects:"]

        for i, project in enumerate(projects, 1):
            refs.add_project(i, UUID(project.id))
            lines.append(f"[{i}] Project: {project.name}")

            # Add tasks with letter references
            for j, task in enumerate(project.tasks):
                letter = chr(97 + j)  # a, b, c, ...
                refs.add_task(i, letter, UUID(task.id))
                lines.append(
                    f"  [{letter}] {task.title} {task.status_display} " f"[{task.priority_display}]"
                )

        return "\n".join(lines)

    @staticmethod
    def format_task_detail(task: TaskViewModel) -> str:
        """Format detailed task information."""
        lines = [
            f"Task: {task.title}",
            f"Status: {task.status_display}",
            f"Priority: {task.priority_display}",
        ]

        if task.due_date_display:
            lines.append(f"Due Date: {task.due_date_display}")

        if task.description:
            lines.append(f"Description: {task.description}")

        if task.project_display:
            lines.append(f"Project: {task.project_display}")

        return "\n".join(lines)

    @staticmethod
    def format_task_actions() -> Tuple[str, Dict[str, str]]:
        """
        Format task actions menu.

        Returns:
            A tuple containing:
            - Formatted menu string
            - Dictionary mapping action keys to descriptions
        """
        actions: Dict[str, str] = {
            "1": "Edit status",
            "2": "Edit priority",
            "3": "Edit due date",
            "4": "Edit description",
            "5": "Move to project",
            "6": "Complete task",
            "7": "Delete task",
        }

        lines = ["", "Actions:"]
        lines.extend(f"[{k}] {v}" for k, v in actions.items())
        lines.append("Choose an action or press enter to exit?")

        return "\n".join(lines), actions

    @staticmethod
    def format_status_options() -> dict[str, TaskStatus]:
        """Format task status options."""
        return {"1": TaskStatus.TODO, "2": TaskStatus.IN_PROGRESS, "3": TaskStatus.DONE}

    @staticmethod
    def format_priority_options() -> dict[str, Priority]:
        """Format task priority options."""
        return {"1": Priority.LOW, "2": Priority.MEDIUM, "3": Priority.HIGH}
