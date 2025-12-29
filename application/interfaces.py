from typing import Protocol

from domain.order import Order
from domain.money import Money


class OrderRepository(Protocol):
    """Интерфейс репозитория заказов."""
    
    def get_by_id(self, order_id: str) -> Order:
        ...

    def save(self, order: Order) -> None:
        ...


class PaymentGateway(Protocol):
    """Интерфейс платёжного шлюза."""
    
    def charge(self, order_id: str, amount: Money) -> str:
        """Провести платёж и вернуть ID транзакции."""
        ...
