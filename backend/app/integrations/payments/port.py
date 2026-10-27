from typing import Protocol


class PaymentPort(Protocol):
    def charge(self, amount: int, currency: str) -> str: ...
