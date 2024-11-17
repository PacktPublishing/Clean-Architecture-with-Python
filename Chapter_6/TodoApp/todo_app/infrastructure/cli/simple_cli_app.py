from todo_app.infrastructure.config.container import Application


class SimpleCli:
    def __init__(self, app: Application):
        self.app = app
        self.command_aliases = {
            't': 'title',
            'd': 'description',
            'n': 'completion_notes',
        }

    def _normalize_kwargs(self, kwargs: dict) -> dict:
        """Convert short aliases to full parameter names"""
        normalized = {}
        for key, value in kwargs.items():
            # Strip leading dashes and convert to standard format
            clean_key = key.lstrip('-')
            # Use full name if it's an alias, otherwise use the original
            normalized[self.command_aliases.get(clean_key, clean_key)] = value
        return normalized

    def run(self, command: str, **kwargs) -> int:
        normalized_kwargs = self._normalize_kwargs(kwargs)
        
        command_handlers = {
            'create-task': self._handle_create_task,
            'create-project': self._handle_create_project,
            'complete-project': self._handle_complete_project,
        }
        
        handler = command_handlers.get(command)
        if not handler:
            print(f"Unknown command: {command}")
            return 1
            
        return handler(**normalized_kwargs)

    def _handle_create_task(self, title: str = "", description: str = "") -> int:
        result = self.app.task_controller.handle_create(title, description)
        if result.is_success:
            task_vm = self.app.task_presenter.present_task(result.value)
            print(f"{task_vm.status_display} [{task_vm.priority_display}] {task_vm.title}")
            return 0
        print(self.app.task_presenter.present_error(result.error.message))
        return 1

    def _handle_create_project(self, title: str = "", description: str = "") -> int:
        result = self.app.project_controller.handle_create(title, description)
        if result.is_success:
            project_vm = self.app.project_presenter.present_project(result.value)
            print(f"Created project: {project_vm.name}")
            return 0
        print(self.app.project_presenter.present_error(result.error.message))
        return 1

    def _handle_complete_project(self, id: str = "", completion_notes: str = "") -> int:
        result = self.app.project_controller.handle_complete(id, completion_notes)
        if result.is_success:
            project_vm = self.app.project_presenter.present_project(result.value)
            print(f"Completed project: {project_vm.name}")
            return 0
        print(self.app.project_presenter.present_error(result.error.message))
        return 1