"""Email settings service backed by runtime system settings."""
import asyncio
from dataclasses import dataclass, field
import logging
from typing import Optional

import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.schemas.system_settings import RuntimeSettingSource
from app.services.system_settings_service import (
    RuntimeSettingsEncryptionError,
    RuntimeSettingsError,
    RuntimeSettingsService,
)
from app.utils.url_policy import URLPolicyError, validate_public_host


logger = logging.getLogger(__name__)


@dataclass
class EmailSettings:
    """Resolved email settings."""

    enabled: bool = False
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from_email: str = "notifications@workchord.local"
    smtp_use_tls: bool = True
    field_sources: dict[str, RuntimeSettingSource] = field(default_factory=dict)
    password_configured: Optional[bool] = None

    @property
    def has_password(self) -> bool:
        """Return whether an SMTP password is configured."""
        if self.password_configured is not None:
            return self.password_configured
        return bool(self.smtp_password)

    @property
    def is_configured(self) -> bool:
        """Return whether email can be attempted."""
        return self.enabled and bool(self.smtp_host)


class EmailSettingsService:
    """Manage email settings through ``system_settings``."""

    def __init__(self, db: Optional[AsyncSession] = None, settings_override=None):
        self.db = db
        self.settings_override = settings_override

    @classmethod
    def get_instance(cls) -> "EmailSettingsService":
        """Backward-compatible no-DB instance for legacy tests."""
        return EmailSettingsService()

    def get_settings_sync(self, *, include_secret: bool = True) -> EmailSettings:
        """Return disabled settings when no DB session is available."""
        if self.settings_override is None:
            return EmailSettings()
        settings = self.settings_override
        return EmailSettings(
            enabled=settings.notifications_enabled,
            smtp_host=settings.smtp_host,
            smtp_port=settings.smtp_port,
            smtp_user=settings.smtp_user,
            smtp_password=settings.smtp_password if include_secret else "",
            smtp_from_email=settings.smtp_from_email,
            smtp_use_tls=settings.smtp_use_tls,
            password_configured=bool(settings.smtp_password),
        )

    def _allow_private_egress(self) -> bool:
        settings = self.settings_override or get_settings()
        return bool(getattr(settings, "allow_private_egress_urls", False))

    async def get_settings(self, *, include_secret: bool = False) -> EmailSettings:
        """Resolve current email settings."""
        if self.db is None:
            return self.get_settings_sync(include_secret=include_secret)

        runtime = RuntimeSettingsService(self.db, settings_override=self.settings_override)
        resolved = await runtime.get_email_settings(include_secret=include_secret)
        has_password, password_source = await runtime.has_secret("email.smtp_password")
        sources = await runtime._field_sources("email")
        sources["smtp_password"] = password_source
        return EmailSettings(
            enabled=resolved.enabled,
            smtp_host=resolved.smtp_host,
            smtp_port=resolved.smtp_port,
            smtp_user=resolved.smtp_user,
            smtp_password=resolved.smtp_password,
            smtp_from_email=resolved.smtp_from_email,
            smtp_use_tls=resolved.smtp_use_tls,
            field_sources=sources,
            password_configured=has_password,
        )

    async def update_settings(
        self,
        *,
        enabled: bool,
        smtp_host: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: Optional[str],
        smtp_from_email: str,
        smtp_use_tls: bool,
        clear_smtp_password: bool = False,
    ) -> EmailSettings:
        """Update email settings. ``smtp_password=None`` preserves the current secret."""
        if self.db is None:
            raise RuntimeError("A database session is required to update email settings")

        from app.schemas.email_settings import EmailSettingsUpdate

        runtime = RuntimeSettingsService(self.db, settings_override=self.settings_override)
        resolved = await runtime.update_email(
            EmailSettingsUpdate(
                enabled=enabled,
                smtp_host=smtp_host,
                smtp_port=smtp_port,
                smtp_user=smtp_user,
                smtp_password=smtp_password,
                smtp_from_email=smtp_from_email,
                smtp_use_tls=smtp_use_tls,
                clear_smtp_password=clear_smtp_password,
            )
        )
        has_password, password_source = await runtime.has_secret("email.smtp_password")
        sources = await runtime._field_sources("email")
        sources["smtp_password"] = password_source
        return EmailSettings(
            enabled=resolved.enabled,
            smtp_host=resolved.smtp_host,
            smtp_port=resolved.smtp_port,
            smtp_user=resolved.smtp_user,
            smtp_password=resolved.smtp_password,
            smtp_from_email=resolved.smtp_from_email,
            smtp_use_tls=resolved.smtp_use_tls,
            field_sources=sources,
            password_configured=has_password,
        )

    async def test_connection(self, recipient: str) -> tuple[bool, str]:
        """Send a test email using current settings."""
        try:
            settings = await self.get_settings(include_secret=True)
        except RuntimeSettingsEncryptionError as exc:
            return False, str(exc)
        except RuntimeSettingsError as exc:
            return False, str(exc)

        if not settings.smtp_host:
            return False, "SMTP host is not configured"

        try:
            validate_public_host(
                settings.smtp_host,
                allow_private=self._allow_private_egress(),
            )
            message = MIMEMultipart("alternative")
            message["Subject"] = "[WorkChord] Test Email"
            message["From"] = settings.smtp_from_email
            message["To"] = recipient

            body_text = "This is a test email from WorkChord. Your email settings are working correctly!"
            body_html = """
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #3b82f6;">Email Configuration Test</h2>
                <p>This is a test email from <strong>WorkChord</strong>.</p>
                <p>Your email settings are working correctly.</p>
                <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;" />
                <p style="color: #6b7280; font-size: 12px;">
                    SMTP Server: {host}:{port}<br />
                    TLS: {tls}
                </p>
            </body>
            </html>
            """.format(
                host=settings.smtp_host,
                port=settings.smtp_port,
                tls="Enabled" if settings.smtp_use_tls else "Disabled",
            )

            message.attach(MIMEText(body_text, "plain", "utf-8"))
            message.attach(MIMEText(body_html, "html", "utf-8"))

            await asyncio.wait_for(
                aiosmtplib.send(
                    message,
                    hostname=settings.smtp_host,
                    port=settings.smtp_port,
                    username=settings.smtp_user or None,
                    password=settings.smtp_password or None,
                    start_tls=settings.smtp_use_tls,
                    timeout=5,
                ),
                timeout=5,
            )
            return True, f"Test email sent successfully to {recipient}"

        except aiosmtplib.SMTPAuthenticationError:
            return False, "Authentication failed. Check your username and password."
        except aiosmtplib.SMTPConnectError:
            return False, "Could not connect to SMTP server. Check host and port."
        except URLPolicyError as exc:
            return False, str(exc)
        except Exception as exc:
            # The Settings test action is an SMTP provider boundary. Preserve
            # its existing response while recording the internal failure.
            logger.error(
                "SMTP settings test failed",
                exc_info=True,
                extra={"operation": "email_settings_test"},
            )
            return False, f"Failed to send email: {str(exc)}"
