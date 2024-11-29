import click
from todo_app.interfaces.view_models.base import OperationResult
from todo_app.interfaces.view_models.project_vm import ProjectViewModel
from todo_app.infrastructure.config.container import Application


class ClickCli:
    def __init__(self, app: Application):
        self.app = app
        self.cli = click.Group()
        
        # Create command instances bound to self
        create_task_cmd = click.Command(
            'create-task',
            callback=self.create_task,
            params=[
                click.Option(["-t", "--title"], required=True, help="Task title"),
                click.Option(["-d", "--description"], default="", help="Task description")
            ]
        )
        
        create_project_cmd = click.Command(
            'create-project',
            callback=self.create_project,
            params=[
                click.Option(["-t", "--title"], required=True, help="Project title"),
                click.Option(["-d", "--description"], default="", help="Project description")
            ]
        )
        
        complete_project_cmd = click.Command(
            'complete-project',
            callback=self.complete_project,
            params=[
                click.Option(["--id"], required=True, help="Project ID"),
                click.Option(["-n", "--completion-notes"], default="", help="Completion notes")
            ]
        )

        # Add commands to the group
        self.cli.add_command(create_task_cmd)
        self.cli.add_command(create_project_cmd)
        self.cli.add_command(complete_project_cmd)

    def run(self) -> int:
        """Entry point for running the Click CLI application"""
        try:
            return self.cli.main(standalone_mode=False)
        except Exception as e:
            click.secho(str(e), fg='red', err=True)
            return 1

    def create_task(self, title: str, description: str):
        result = self.app.task_controller.handle_create(title, description)
        
        if result.is_success:
            task = result.success
            click.echo(f"{task.status_display} [{task.priority_display}] {task.title}")
            return 0
            
        click.secho(result.error.message, fg='red', err=True)
        return 1

    def create_project(self, title: str, description: str):
        result: OperationResult[ProjectViewModel] = self.app.project_controller.handle_create(title, description)
        
        if result.is_success:
            project_vm = result.success
            click.echo(f"Created project: {project_vm.name}")
            return 0
        click.secho(result.error.message, fg='red', err=True)
        return 1

    def complete_project(self, id: str, completion_notes: str):
        result = self.app.project_controller.handle_complete(id, completion_notes)
        if result.is_success:
            project_vm = result.success
            click.echo(f"Completed project: {project_vm.name}")
            return 0
        click.secho(result.error.message, fg='red', err=True)
        return 1
