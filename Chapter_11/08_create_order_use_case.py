# order_system/application/use_cases/create_order.py
from dataclasses import dataclass
from typing import List, Dict, Any
from uuid import UUID


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

            # ... inventory validation logic ...

            # Update inventory
            product.decrease_stock(quantity)
            self.product_repository.update(product)

        # Process payment
        payment_result = self.payment_service.process_payment(order)
        if not payment_result.success:
            raise ValueError(f"Payment failed: {payment_result.error_message}")
        
        # Mark order as paid and save
        order.mark_as_paid()
        self.order_repository.save(order)
        
        return order
