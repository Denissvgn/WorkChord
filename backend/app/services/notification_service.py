"""Email notification service for task status changes."""
import asyncio
import logging
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import aiosmtplib

from app.services.email_settings_service import EmailSettingsService
from app.services.language_service import (
    notification_overdue_body_html,
    notification_overdue_subject,
    notification_status_change_body_html,
    notification_status_change_subject,
    resolve_runtime_ui_language,
)

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for sending email notifications about task status changes."""

    def __init__(self, db=None):
        self.db = db
        self._settings_service = EmailSettingsService(db)

    @property
    def settings(self):
        """Get environment-backed settings for sync legacy callers."""
        return self._settings_service.get_settings_sync()

    @property
    def is_enabled(self) -> bool:
        """Check env-backed notification state for sync legacy callers."""
        settings = self.settings
        return settings.enabled and bool(settings.smtp_host)

    async def _settings(self):
        """Get current runtime settings."""
        return await self._settings_service.get_settings(include_secret=True)

    async def _ui_language(self):
        """Resolve the runtime UI language used for generated notification text."""
        return await resolve_runtime_ui_language(self.db)

    async def send_email(
        self,
        recipients: list[str],
        subject: str,
        body_html: str,
        body_text: Optional[str] = None
    ) -> bool:
        """
        Send an email to the specified recipients.

        Returns True if sent successfully, False otherwise.
        """
        try:
            settings = await self._settings()
        except Exception:
            logger.error(
                "[Notification] Failed to resolve email settings",
                exc_info=True,
            )
            return False
        if not settings.is_configured:
            logger.info(f"[Notification] Email disabled. Would send to {recipients}: {subject}")
            return False

        if not recipients:
            logger.warning("[Notification] No recipients specified")
            return False

        # Filter out empty/None recipients
        valid_recipients = [r for r in recipients if r]
        if not valid_recipients:
            logger.warning("[Notification] No valid recipients after filtering")
            return False

        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = settings.smtp_from_email
            message["To"] = ", ".join(valid_recipients)

            # Plain text fallback
            if body_text:
                message.attach(MIMEText(body_text, "plain", "utf-8"))

            # HTML body
            message.attach(MIMEText(body_html, "html", "utf-8"))

            await asyncio.wait_for(
                aiosmtplib.send(
                    message,
                    hostname=settings.smtp_host,
                    port=settings.smtp_port,
                    username=settings.smtp_user or None,
                    password=settings.smtp_password or None,
                    start_tls=settings.smtp_use_tls,
                    timeout=3,
                ),
                timeout=3,
            )

            logger.info(f"[Notification] Email sent to {valid_recipients}: {subject}")
            return True

        except Exception:
            # SMTP is an external provider boundary; callers retain the existing
            # False fallback while the failure remains observable server-side.
            logger.error(
                "[Notification] Failed to send email",
                exc_info=True,
                extra={"recipient_count": len(valid_recipients)},
            )
            return False

    async def notify_status_change(
        self,
        task_title: str,
        task_id: int,
        old_status: str,
        new_status: str,
        manager_email: Optional[str],
        assignee_email: Optional[str],
        cascade_updates: list[dict],
        reason: Optional[str] = None
    ) -> bool:
        """
        Send notification about task status change.

        Recipients:
        - Manager (if email set)
        - Assignee (if email set)
        - Assignees of affected tasks (for cascade updates)
        """
        language = await self._ui_language()
        subject = notification_status_change_subject(task_id, old_status, new_status, language)
        body_html = notification_status_change_body_html(
            task_title,
            task_id,
            old_status,
            new_status,
            cascade_updates,
            reason,
            language,
        )

        recipients = [email for email in (manager_email, assignee_email) if email]
        return await self.send_email(recipients, subject, body_html)

    async def notify_overdue(
        self,
        task_title: str,
        task_id: int,
        planned_start: date,
        manager_email: Optional[str],
        assignee_email: Optional[str]
    ) -> bool:
        """Send notification about overdue task start."""
        today = date.today()
        days_overdue = (today - planned_start).days
        language = await self._ui_language()
        subject = notification_overdue_subject(task_id, days_overdue, language)
        body_html = notification_overdue_body_html(task_title, task_id, planned_start, days_overdue, language)

        recipients = [email for email in (manager_email, assignee_email) if email]
        return await self.send_email(recipients, subject, body_html)


# Singleton instance
_notification_service: Optional[NotificationService] = None


def get_notification_service(db=None) -> NotificationService:
    """Get or create notification service instance."""
    global _notification_service
    if db is not None:
        return NotificationService(db)
    if _notification_service is None:
        _notification_service = NotificationService()
    return _notification_service
