from app.integrations.notifications.providers.console import ConsoleProvider

_provider = ConsoleProvider()


def send(to: str, message: str) -> None:
    _provider.send(to, message)
