# order_system/application/use_cases/create_order.py
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from uuid import UUID

from ...domain.entities.order import Order, OrderItem
from ...domain.repositories.order_repository import OrderRepository
from ...domain.repositories.product_repository import ProductRepository
from ...domain.services.payment_service import PaymentService, PaymentResult


@dataclass
class CreateOrderRequest:
    customer_id: UUID
    items: List[Dict[str, Any]]


@dataclass
class CreateOrderUseCase:
    order_repository: OrderRepository
    product_repository: ProductRepository
    payment_service: PaymentService

    def execute(self, request: CreateOrderRequest) -> Order:
        # Create order entity with basic information
        order = Order(customer_id=request.customer_id)

        # Add items to order, checking inventory
        for item_data in request.items:
            product_id = UUID(item_data["product_id"])
            quantity = item_data["quantity"]

            # Get product and check inventory
            product = self.product_repository.get_by_id(product_id)
            if not product:
                raise ValueError(f"Product with ID {product_id} not found")

            # Update inventory
            product.decrease_stock(quantity)
            self.product_repository.update(product)

            # Add item to order
            order_item = OrderItem(product_id=product_id, quantity=quantity, price=product.price)
            order.add_item(order_item)

        # Process payment
        payment_result = self.payment_service.process_payment(order)
        if not payment_result.success:
            raise ValueError(f"Payment failed: {payment_result.error_message}")

        # Mark order as paid and save
        order.mark_as_paid()
        self.order_repository.save(order)

        return order
