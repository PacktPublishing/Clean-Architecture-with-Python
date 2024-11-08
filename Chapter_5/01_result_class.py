from dataclasses import dataclass
from typing import Any, Optional

from Chapter_5.ToDoApp.todo_app.application.common.result import Error


@dataclass(frozen=True)
class Result:
    """Represents success or failure of a use case execution"""

    value: Any = None
    error: Optional[Error] = None

    @property
    def is_success(self) -> bool:
        return self.error is None

    @classmethod
    def success(cls, value: Any) -> "Result":
        return cls(value=value)

    @classmethod
    def failure(cls, error: Error) -> "Result":
        return cls(error=error)


"""
This Result pattern enables clean orchestration of domain operations, as demonstrated in this usage example:

try:
    project = find_project(project_id)
   	task = create_task(task_details)
    project.add_task(task)
   	notify_stakeholders(task)
    return Result.success(TaskResponse.from_entity(task))
except ProjectNotFoundError:
   	return Result.failure(Error.not_found("Project", str(project_id)))
except ValidationError as e:
   	return Result.failure(Error.validation_error(str(e)))
"""
