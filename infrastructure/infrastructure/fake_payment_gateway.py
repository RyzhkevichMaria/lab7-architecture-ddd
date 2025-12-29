from application.interfaces import PaymentGateway
from domain.money import Money


class FakePaymentGateway(PaymentGateway):
    """Фейковый платёжный шлюз для тестов."""

    def __init__(self):
        self.charges = []

    def charge(self, order_id: str, amount: Money) -> str:
        self.charges.append((order_id, amount))
        return f"tx-{order_id}"
