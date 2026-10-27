from typing import Protocol


class NotificationPort(Protocol):
    def send(self, to: str, message: str) -> None: ...
