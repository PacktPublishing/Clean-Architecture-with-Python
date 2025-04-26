# Task management Request model - internal only
class CreateTaskRequest:
    """Data structure for task creation requests."""

    title: str
    description: str
    project_id: Optional[str] = None

    def to_execution_params(self) -> dict:
        """Convert validated request data to use case parameters."""
        return {
            "title": self.title.strip(),
            "project_id": UUID(self.project_id) if self.project_id else None,
            "description": self.description.strip(),
        }


# API Request DTO - now a public contract
class CreateTaskRequest:
    title: str
    description: str
    project_id: Optional[str] = None
