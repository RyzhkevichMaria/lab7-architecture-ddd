import pytest

from domain.money import Money
from domain.order import Order
from domain.order_line import OrderLine
from domain.order_status import OrderStatus

from application.pay_order_use_case import PayOrderUseCase

from infrastructure.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.fake_payment_gateway import FakePaymentGateway


def create_order_with_one_line(order_id="order-1"):
    order = Order(order_id=order_id)
    order.add_line(
        OrderLine(
            product_id="p1",
            quantity=2,
            price=Money(500)
        )
    )
    return order


def test_successful_payment():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()

    order = create_order_with_one_line()
    repo.save(order)

    use_case = PayOrderUseCase(repo, gateway)

    transaction_id = use_case.execute(order.order_id)

    assert transaction_id == "tx-order-1"
    assert order.status == OrderStatus.PAID
    assert len(gateway.charges) == 1


def test_cannot_pay_empty_order():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()

    order = Order(order_id="empty")
    repo.save(order)

    use_case = PayOrderUseCase(repo, gateway)

    with pytest.raises(ValueError):
        use_case.execute(order.order_id)


def test_cannot_pay_twice():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()

    order = create_order_with_one_line()
    repo.save(order)

    use_case = PayOrderUseCase(repo, gateway)

    use_case.execute(order.order_id)

    with pytest.raises(ValueError):
        use_case.execute(order.order_id)


def test_cannot_modify_paid_order():
    order = create_order_with_one_line()
    order.pay()

    with pytest.raises(ValueError):
        order.add_line(
            OrderLine(
                product_id="p2",
                quantity=1,
                price=Money(100)
            )
        )


def test_total_amount_is_correct():
    order = Order(order_id="total-test")

    order.add_line(
        OrderLine("p1", 2, Money(300))
    )
    order.add_line(
        OrderLine("p2", 1, Money(400))
    )

    assert order.total == Money(1000)
