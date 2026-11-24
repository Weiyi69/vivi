import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Protocol

from app.core.config import Settings


class EmailDeliveryError(RuntimeError):
    pass


class EmailDelivery(Protocol):
    def send(self, recipient: str, subject: str, body: str) -> None:
        """Deliver an email."""


class DevelopmentOutbox:
    def __init__(self, root: str) -> None:
        self.root = Path(root)

    def send(self, recipient: str, subject: str, body: str) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        index = sum(1 for path in self.root.glob("*.txt") if path.is_file()) + 1
        content = f"To: {recipient}\nSubject: {subject}\n\n{body}\n"
        (self.root / f"{index:04d}.txt").write_text(content, encoding="utf-8")


class SmtpDelivery:
    def __init__(self, settings: Settings) -> None:
        if not settings.smtp_host or not settings.smtp_from:
            raise EmailDeliveryError("SMTP_HOST and SMTP_FROM must be configured")
        self.settings = settings
        self.smtp_host: str = settings.smtp_host

    def send(self, recipient: str, subject: str, body: str) -> None:
        message = EmailMessage()
        message["From"] = self.settings.smtp_from
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        try:
            if self.settings.smtp_use_tls:
                with smtplib.SMTP(
                    self.smtp_host, self.settings.smtp_port, timeout=10
                ) as server:
                    server.starttls()
                    if self.settings.smtp_username:
                        server.login(
                            self.settings.smtp_username,
                            self.settings.smtp_password or "",
                        )
                    server.send_message(message)
            else:
                with smtplib.SMTP(
                    self.smtp_host, self.settings.smtp_port, timeout=10
                ) as server:
                    if self.settings.smtp_username:
                        server.login(
                            self.settings.smtp_username,
                            self.settings.smtp_password or "",
                        )
                    server.send_message(message)
        except (smtplib.SMTPException, TimeoutError, OSError) as exc:
            raise EmailDeliveryError("Email delivery failed") from exc


def get_email_delivery(settings: Settings) -> EmailDelivery:
    if settings.app_env == "production" and settings.email_mode != "smtp":
        raise EmailDeliveryError("Production SMTP delivery must be configured")
    if settings.email_mode == "smtp":
        return SmtpDelivery(settings)
    if settings.app_env == "production":
        raise EmailDeliveryError("Development email delivery is disabled in production")
    return DevelopmentOutbox(settings.development_outbox_dir)
