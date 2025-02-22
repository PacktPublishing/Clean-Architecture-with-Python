# todo_app/application/use_cases/task_use_cases.py
import logging

logger = logging.getLogger(__name__)

@dataclass
class CreateTaskUseCase:
    task_repository: TaskRepository
    project_repository: ProjectRepository

    def execute(self, request: CreateTaskRequest) -> Result:
        try:
            logger.info(
                "Creating new task",
                extra={"title": request.title, "project_id": request.project_id},
            )
            # ... implementation continues ...
