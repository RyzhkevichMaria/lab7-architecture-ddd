from typing import Dict

from domain.order import Order
from application.interfaces import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    """Репозиторий заказов в памяти."""
    
    def __init__(self):
        self._orders: Dict[str, Order] = {}

    def get_by_id(self, order_id: str) -> Order:
        if order_id not in self._orders:
            raise ValueError(f"Order with id {order_id} not found")
        return self._orders[order_id]

    def save(self, order: Order) -> None:
        self._orders[order.order_id] = order
