from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class DeletionOutcome:
    """Represents the result of a deletion operation."""

    entity_id: UUID

    def __str__(self) -> str:
        return f"Successfully deleted entity with ID: {self.entity_id}"
