from dataclasses import dataclass

from .money import Money


@dataclass(frozen=True)
class OrderLine:
    """Строка заказа — часть агрегата Order."""
    product_id: str
    quantity: int
    price: Money

    def total(self) -> Money:
        """Сумма по строке: цена × количество."""
        amount = self.price.amount * self.quantity
        return Money(amount, self.price.currency)

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
