# order_system/domain/repositories/product_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """Retrieve a product by its ID"""
        pass

    @abstractmethod
    def save(self, product: Product) -> None:
        """Save a product to the repository"""
        pass

    @abstractmethod
    def get_all(self) -> List[Product]:
        """Retrieve all products"""
        pass

    @abstractmethod
    def update(self, product: Product) -> None:
        """Update a product"""
        pass
