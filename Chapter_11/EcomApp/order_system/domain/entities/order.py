# order_system/domain/entities/order.py
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4


class OrderStatus(Enum):
    CREATED = "CREATED"
    PAID = "PAID"
    FULFILLING = "FULFILLING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"


@dataclass
class OrderItem:
    product_id: UUID
    quantity: int
    price: float

    @property
    def total_price(self) -> float:
        return self.price * self.quantity


@dataclass
class Order:
    customer_id: UUID
    items: List[OrderItem] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    status: OrderStatus = OrderStatus.CREATED
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = None

    @property
    def total_price(self) -> float:
        return sum(item.total_price for item in self.items)

    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)
        self.updated_at = datetime.now()

    def mark_as_paid(self) -> None:
        if self.status != OrderStatus.CREATED:
            raise ValueError(f"Cannot mark as paid: order is {self.status.value}")
        self.status = OrderStatus.PAID
        self.updated_at = datetime.now()
