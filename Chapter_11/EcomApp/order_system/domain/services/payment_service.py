# order_system/domain/services/payment_service.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from ..entities.order import Order


@dataclass
class PaymentResult:
    success: bool
    error_message: Optional[str] = None


class PaymentService(ABC):
    @abstractmethod
    def process_payment(self, order: Order) -> PaymentResult:
        """Process payment for an order"""
        pass
