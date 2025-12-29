from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    """Value Object для суммы денег (иммутабельный)."""
    amount: int  # в копейках, чтобы избежать проблем с float
    currency: str = "USD"

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount and self.currency == other.currency

    def __str__(self) -> str:
        return f"{self.amount / 100:.2f} {self.currency}"
