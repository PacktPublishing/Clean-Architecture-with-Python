from dataclasses import dataclass

from Chapter_5.ToDoApp.todo_app.application.common.result import Result, Error
from Chapter_5.ToDoApp.todo_app.application.dtos.project_dtos import (
    CompleteProjectRequest,
    ProjectCompletionResponse,
)
from Chapter_5.ToDoApp.todo_app.application.repositories.project_repository import (
    ProjectRepository,
)
from Chapter_5.ToDoApp.todo_app.domain.exceptions import (
    ValidationError,
    ProjectNotFoundError,
)


@dataclass
class CompleteProjectUseCase:
    """Use case for marking a project as complete."""

    project_repository: ProjectRepository

    def execute(self, request: CompleteProjectRequest) -> Result:
        """Execute the use case."""
        try:
            params = request.to_execution_params()

            project = self.project_repository.get(params["project_id"])
            project.mark_completed(notes=params["completion_notes"])

            self.project_repository.save(project)

            response = ProjectCompletionResponse.from_entity(project)
            return Result.success(response)

        except ProjectNotFoundError:
            return Result.failure(
                Error.not_found("Project", str(params["project_id"]))
            )
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
