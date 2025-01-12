# 1. Domain Layer: Add ProjectType and update entities
from dataclasses import dataclass, field
from uuid import UUID


class ProjectType(Enum):
    REGULAR = "REGULAR"
    INBOX = "INBOX"


@dataclass
class Project(Entity):
    name: str
    description: str = ""
    project_type: ProjectType = field(default=ProjectType.REGULAR)

    @classmethod
    def create_inbox(cls) -> "Project":
        return cls(
            name="INBOX",
            description="Default project for unassigned tasks",
            project_type=ProjectType.INBOX,
        )


@dataclass
class Task(Entity):
    title: str
    description: str
    project_id: UUID  # No longer optional
