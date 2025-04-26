# Task management - manual validation
class CreateTaskRequest:
    """Request data for creating a new task."""

    title: str
    description: str

    def __post_init__(self):
        if not self.title.strip():
            raise ValueError("Title cannot be empty")

    def to_execution_params(self) -> dict:
        return {"title": self.title.strip(), "description": self.description.strip()}


# FastAPI/Pydantic - automatic validation
from pydantic import BaseModel, Field


class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1)
    description: str
