# order_system/infrastructure/services/dummy_payment_service.py
from ...domain.entities.order import Order
from ...domain.services.payment_service import PaymentService, PaymentResult


class DummyPaymentService(PaymentService):
    def process_payment(self, order: Order) -> PaymentResult:
        # In a real implementation, this would call an external payment gateway
        # For this demo, we'll just simulate a successful payment
        return PaymentResult(success=True)
