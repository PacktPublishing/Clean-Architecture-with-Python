# 2. Application Layer: Update repository interface and use cases
class ProjectRepository(ABC):
    @abstractmethod
    def get_inbox(self) -> Project:
        """Get the INBOX project."""
        pass

@dataclass
class CreateTaskUseCase:
    task_repository: TaskRepository
    project_repository: ProjectRepository

    def execute(self, request: CreateTaskRequest) -> Result:
        try:
            params = request.to_execution_params()
            project_id = params.get("project_id")
            if not project_id:
                project_id = self.project_repository.get_inbox().id
            # ... remainder of implementation