class EmailSmtpProvider:
    def send(self, to: str, message: str) -> None:
        raise NotImplementedError("SMTP is not configured")
