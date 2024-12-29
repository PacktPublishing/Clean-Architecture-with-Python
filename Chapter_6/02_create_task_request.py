from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CreateTaskRequest:
    """Request data for creating a new task."""

    title: str

    description: str

    due_date: Optional[str] = None

    priority: Optional[str] = None

    def to_execution_params(self) -> dict:
        """Convert request data to use case parameters."""

        params = {
            "title": self.title.strip(),
            "description": self.description.strip(),
        }

        if self.priority:

            params["priority"] = Priority[self.priority.upper()]

        return params


"""
# In TaskController 

try: 

    request = CreateTaskRequest(title=title, description=description) 

    # Request is now validated and properly formatted 

    result = self.create_use_case.execute(request) 

except ValueError as e: 

    # Handle validation errors before they reach use cases 

    return OperationResult.fail(str(e), "VALIDATION_ERROR") 

"""
