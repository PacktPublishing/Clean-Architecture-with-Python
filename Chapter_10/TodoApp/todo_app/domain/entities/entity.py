from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Entity:
    # Automatically generates a unique UUID for the 'id' field;
    #   excluded from the __init__ method
    id: UUID = field(default_factory=uuid4, init=False)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
