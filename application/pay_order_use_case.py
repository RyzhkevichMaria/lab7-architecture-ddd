from dataclasses import dataclass

from domain.order import Order
from domain.money import Money

from .interfaces import OrderRepository, PaymentGateway


@dataclass
class PayOrderUseCase:
    """Use-case: оплата заказа."""
    order_repository: OrderRepository
    payment_gateway: PaymentGateway

    def execute(self, order_id: str) -> str:
        """Выполняет оплату и возвращает ID транзакции."""
        # 1. Загружаем заказ
        order: Order = self.order_repository.get_by_id(order_id)

        # 2. Доменная операция оплаты
        order.pay()

        # 3. Проводим платёж через шлюз
        transaction_id = self.payment_gateway.charge(order_id, order.total)

        # 4. Сохраняем заказ
        self.order_repository.save(order)

        return transaction_id
