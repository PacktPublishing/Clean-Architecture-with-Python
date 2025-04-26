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
            
            # ... task creation logic ...
            
            logger.info(
                "Task created successfully",
                extra={"context":{
                    "task_id": str(task.id),
                    "project_id": str(project_id),
                    "priority": task.priority.name,
                }},
            )
            # ... remainder of method