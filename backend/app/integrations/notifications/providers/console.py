class ConsoleProvider:
    def send(self, to: str, message: str) -> None:
        print(f"[notify:{to}] {message}")
