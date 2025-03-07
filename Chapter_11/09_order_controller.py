# order_system/interfaces/controllers/order_controller.py
from dataclasses import dataclass
from typing import Dict, Any
from uuid import UUID

@dataclass
class OrderController:
    create_use_case: CreateOrderUseCase
    
    def handle_create_order(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Transform web request to domain request format
            customer_id = UUID(request_data['customer_id'])
            items = request_data['items']
            
            request = CreateOrderRequest(
                customer_id=customer_id,
                items=items
            )
            
            # Execute use case
            order = self.create_use_case.execute(request)
            
            # Transform domain response to web response format
            return {
                'order_id': str(order.id),
                'status': order.status.value
            }
        except ValueError as e:
            # ... exception logic   