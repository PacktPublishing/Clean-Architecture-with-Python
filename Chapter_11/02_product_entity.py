from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Product:
    name: str
    price: float
    stock: int
    id: UUID = field(default_factory=uuid4)

    def decrease_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if quantity > self.stock:
            raise ValueError(f"Insufficient stock: requested {quantity}, available {self.stock}")
        self.stock -= quantity
