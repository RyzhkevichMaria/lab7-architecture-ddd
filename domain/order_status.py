from enum import StrEnum, auto


class OrderStatus(StrEnum):
    """Статусы заказа."""
    DRAFT = auto()      # черновик
    PAID = auto()       # оплачен
    CANCELLED = auto()  # отменён
