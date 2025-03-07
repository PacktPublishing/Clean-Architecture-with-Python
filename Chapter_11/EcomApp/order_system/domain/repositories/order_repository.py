# order_system/domain/repositories/order_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.order import Order


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None:
        """Save an order to the repository"""
        pass

    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        """Retrieve an order by its ID"""
        pass

    @abstractmethod
    def get_by_customer(self, customer_id: UUID) -> List[Order]:
        """Retrieve all orders for a customer"""
        pass
