"""Outbound webhook target management and delivery service."""
import asyncio
import hashlib
import hmac
import json
import logging
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Any, Optional, Sequence
from uuid import uuid4

import httpx
from sqlalchemy import or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database_runtime import run_database_retry
from app.maintenance import require_background_writes_enabled
from app.models.outbound_webhook import (
    OutboundDeliveryChannel,
    OutboundWebhookDelivery,
    OutboundWebhookDeliveryStatus,
    OutboundWebhookEvent,
    OutboundWebhookTarget,
)
from app.services.email_settings_service import EmailSettingsService
from app.services.notification_service import NotificationService
from app.schemas.outbound_webhook import (
    OutboundWebhookDeliveryResponse,
    OutboundWebhookRetryResponse,
    OutboundWebhookTargetCreate,
    OutboundWebhookTargetResponse,
    OutboundWebhookTargetUpdate,
)
from app.utils.time import as_utc, utc_now
from app.utils.url_policy import URLPolicyError, normalize_external_http_url
from app.runtime_telemetry import activity, metrics


logger = logging.getLogger(__name__)


WEBHOOK_EVENT_DOMAINS = {
    "agent",
    "external_link",
    "github",
    "project",
    "release",
    "request_source",
    "task",
    "triage",
    "webhook",
}

KNOWN_WEBHOOK_EVENT_TYPES = {
    "agent.claim_released",
    "agent.claim_renewed",
    "agent.run_created",
    "agent.run_event_created",
    "agent.run_finished",
    "agent.routing.assessment_created",
    "agent.routing.assignment_selected",
    "agent.routing.configured_observed_mismatch",
    "agent.routing.no_eligible_candidate",
    "agent.routing.preview_recorded",
    "agent.routing.rework_created",
    "agent.routing.stale_conflict",
    "agent.routing.tier_escalated",
    "agent.routing.verifier_rejected",
    "agent.task_event_created",
    "external_link.created",
    "external_link.deleted",
    "external_link.github_created",
    "external_link.updated",
    "github.pr_closed",
    "github.pr_edited",
    "github.pr_merged",
    "github.pr_opened",
    "github.pr_ready_for_review",
    "github.pr_reopened",
    "github.pr_synchronize",
    "github.status_automation_failed",
    "project.created",
    "project.deleted",
    "project.health_updated",
    "project.initiative_created",
    "project.initiative_deleted",
    "project.initiative_updated",
    "project.updated",
    "release.created",
    "release.shipped",
    "release.updated",
    "request_source.linked",
    "request_source.unlinked",
    "task.claimed",
    "task.closed",
    "task.created",
    "task.deleted",
    "task.merged",
    "task.resolved",
    "task.status_changed",
    "task.updated",
    "triage.accepted",
    "triage.classification_suggested",
    "triage.converted",
    "triage.created",
    "triage.declined",
    "triage.duplicate_marked",
    "triage.snoozed",
    "triage.updated",
    "webhook.test",
}

RESERVED_DELIVERY_HEADERS = {
    "content-type",
    "x-workchord-delivery-id",
    "x-workchord-event",
    "x-workchord-event-id",
    "x-workchord-signature-256",
}

MAX_RESPONSE_BODY_LENGTH = 2000
DEFAULT_MAX_ATTEMPTS = 5
DEFAULT_RETRY_BASE_SECONDS = 30
DEFAULT_RETRY_MAX_SECONDS = 3600
# The provider timeout budget is currently 30 seconds. A lease must outlive
# that full I/O boundary plus acknowledgement/finalization headroom, otherwise
# a healthy slow provider could make the same attempt claimable twice.
DEFAULT_LEASE_SECONDS = 120


class OutboundWebhookValidationError(ValueError):
    """Raised when outbound webhook input is invalid."""


class OutboundWebhookNotFoundError(LookupError):
    """Raised when an outbound webhook target or delivery cannot be found."""


class OutboundDeliveryAttemptError(RuntimeError):
    """Classify a transport failure as retryable or terminal."""

    def __init__(self, message: str, *, retryable: bool):
        self.retryable = retryable
        super().__init__(message)


class OutboundWebhookService:
    """Manage outbound webhook targets and deliver matching domain events."""

    def __init__(
        self,
        db: AsyncSession,
        *,
        transport: Optional[httpx.AsyncBaseTransport] = None,
        timeout_seconds: float = 5.0,
        notification_service: Optional[NotificationService] = None,
        retry_base_seconds: int = DEFAULT_RETRY_BASE_SECONDS,
        retry_max_seconds: int = DEFAULT_RETRY_MAX_SECONDS,
        lease_seconds: int = DEFAULT_LEASE_SECONDS,
    ):
        self.db = db
        self.transport = transport
        self.timeout_seconds = timeout_seconds
        self.notification_service = notification_service or NotificationService(db)
        self.retry_base_seconds = retry_base_seconds
        self.retry_max_seconds = retry_max_seconds
        self.lease_seconds = lease_seconds

    def _enum_value(self, value: Any) -> Any:
        return value.value if hasattr(value, "value") else value

    @staticmethod
    def _lease_token(worker_id: str) -> str:
        """Return a PostgreSQL-safe token within the model's 64-char column."""
        worker_digest = hashlib.sha256(worker_id.encode("utf-8")).hexdigest()[:16]
        return f"{worker_digest}:{uuid4().hex}"

    def _json_safe(self, value: Any) -> Any:
        """Convert domain payloads into values accepted by SQL JSON columns."""
        def fallback(item: Any) -> Any:
            if isinstance(item, Enum):
                return item.value
            if isinstance(item, (date, datetime)):
                return item.isoformat()
            return str(item)

        return json.loads(json.dumps(value, default=fallback))

    def _target_response(self, target: OutboundWebhookTarget) -> OutboundWebhookTargetResponse:
        """Build a target response without exposing the secret."""
        return OutboundWebhookTargetResponse(
            id=target.id,
            name=target.name,
            description=target.description,
            url=target.url,
            enabled=target.enabled,
            subscribed_events_json=target.subscribed_events_json or [],
            has_secret=bool(target.secret),
            headers_json=target.headers_json or {},
            created_at=target.created_at,
            updated_at=target.updated_at,
        )

    def _delivery_response(self, delivery: OutboundWebhookDelivery) -> OutboundWebhookDeliveryResponse:
        """Build a delivery response from a loaded delivery model."""
        return OutboundWebhookDeliveryResponse.model_validate(delivery)

    def _normalize_subscriptions(self, subscriptions: Sequence[str]) -> list[str]:
        """Validate and deduplicate exact event and wildcard subscription tokens."""
        normalized: list[str] = []
        seen: set[str] = set()
        for raw_token in subscriptions or []:
            token = str(raw_token).strip()
            if not token or token in seen:
                continue
            if token == "*":
                normalized.append(token)
                seen.add(token)
                continue
            if token.endswith(".*"):
                domain = token[:-2]
                if domain not in WEBHOOK_EVENT_DOMAINS:
                    raise OutboundWebhookValidationError(f"Unsupported webhook event domain: {domain}")
                normalized.append(token)
                seen.add(token)
                continue
            if token not in KNOWN_WEBHOOK_EVENT_TYPES:
                raise OutboundWebhookValidationError(f"Unsupported webhook event: {token}")
            normalized.append(token)
            seen.add(token)
        return normalized

    def _normalize_headers(self, headers: dict[str, Any]) -> dict[str, str]:
        """Normalize custom headers and protect reserved delivery headers."""
        normalized: dict[str, str] = {}
        for key, value in (headers or {}).items():
            name = str(key).strip()
            if not name:
                raise OutboundWebhookValidationError("Header names must be non-empty")
            if name.lower() in RESERVED_DELIVERY_HEADERS:
                raise OutboundWebhookValidationError(f"Header {name} is managed by the webhook service")
            normalized[name] = str(value)
        return normalized

    def _event_matches(self, event_type: str, subscriptions: Sequence[str]) -> bool:
        """Return whether a target subscription list includes an event."""
        if "*" in subscriptions:
            return True
        if event_type in subscriptions:
            return True
        domain = event_type.split(".", 1)[0]
        return f"{domain}.*" in subscriptions

    def _delivery_payload(self, event: OutboundWebhookEvent) -> dict[str, Any]:
        """Build the public delivery payload."""
        return {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "entity_type": event.entity_type,
            "entity_id": event.entity_id,
            "occurred_at": event.occurred_at.isoformat(),
            "data": event.payload_json or {},
        }

    def _body_bytes(self, payload: dict[str, Any]) -> bytes:
        """Serialize payload exactly once for signing and sending."""
        return json.dumps(payload, separators=(",", ":"), default=str).encode("utf-8")

    def _signature_header(self, secret: str, body: bytes) -> str:
        digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
        return f"sha256={digest}"

    async def list_targets(self) -> list[OutboundWebhookTargetResponse]:
        """List outbound webhook targets in stable Settings order."""
        result = await self.db.execute(
            select(OutboundWebhookTarget).order_by(
                OutboundWebhookTarget.created_at.desc(),
                OutboundWebhookTarget.id.desc(),
            )
        )
        return [self._target_response(target) for target in result.scalars().all()]

    async def get_target(self, target_id: int) -> Optional[OutboundWebhookTarget]:
        """Load one target by ID."""
        result = await self.db.execute(
            select(OutboundWebhookTarget).where(OutboundWebhookTarget.id == target_id)
        )
        return result.scalar_one_or_none()

    async def create_target(self, data: OutboundWebhookTargetCreate) -> OutboundWebhookTargetResponse:
        """Create a webhook target."""
        target = OutboundWebhookTarget(
            name=data.name.strip(),
            description=data.description,
            url=data.url,
            enabled=data.enabled,
            subscribed_events_json=self._normalize_subscriptions(data.subscribed_events_json),
            secret=data.secret or None,
            headers_json=self._normalize_headers(data.headers_json),
        )
        self.db.add(target)
        await self.db.commit()
        await self.db.refresh(target)
        return self._target_response(target)

    async def update_target(
        self,
        target_id: int,
        data: OutboundWebhookTargetUpdate,
    ) -> Optional[OutboundWebhookTargetResponse]:
        """Apply a partial target update."""
        target = await self.get_target(target_id)
        if target is None:
            return None

        update_data = data.model_dump(exclude_unset=True)
        if "name" in update_data and update_data["name"] is not None:
            target.name = update_data["name"].strip()
        if "description" in update_data:
            target.description = update_data["description"]
        if "url" in update_data and update_data["url"] is not None:
            target.url = update_data["url"]
        if "enabled" in update_data and update_data["enabled"] is not None:
            target.enabled = update_data["enabled"]
        if "subscribed_events_json" in update_data and update_data["subscribed_events_json"] is not None:
            target.subscribed_events_json = self._normalize_subscriptions(
                update_data["subscribed_events_json"]
            )
        if "headers_json" in update_data and update_data["headers_json"] is not None:
            target.headers_json = self._normalize_headers(update_data["headers_json"])
        if "secret" in update_data:
            target.secret = update_data["secret"] or None

        await self.db.commit()
        await self.db.refresh(target)
        return self._target_response(target)

    async def delete_target(self, target_id: int) -> bool:
        """Delete a target while retaining historical delivery rows."""
        target = await self.get_target(target_id)
        if target is None:
            return False

        await self.db.execute(
            update(OutboundWebhookDelivery)
            .where(OutboundWebhookDelivery.target_id == target_id)
            .values(target_id=None)
        )
        await self.db.delete(target)
        await self.db.commit()
        return True

    async def _enabled_targets(self) -> list[OutboundWebhookTarget]:
        result = await self.db.execute(
            select(OutboundWebhookTarget).where(OutboundWebhookTarget.enabled.is_(True))
        )
        return list(result.scalars().all())

    async def _load_delivery(self, delivery_id: int) -> Optional[OutboundWebhookDelivery]:
        result = await self.db.execute(
            select(OutboundWebhookDelivery)
            .options(
                selectinload(OutboundWebhookDelivery.event),
                selectinload(OutboundWebhookDelivery.target),
            )
            .where(OutboundWebhookDelivery.id == delivery_id)
        )
        return result.scalar_one_or_none()

    async def list_deliveries(
        self,
        *,
        target_id: Optional[int] = None,
        status: Optional[str] = None,
        channel: str = OutboundDeliveryChannel.WEBHOOK.value,
        limit: int = 50,
    ) -> list[OutboundWebhookDeliveryResponse]:
        """List recent webhook deliveries."""
        normalized_channel = self._enum_value(channel)
        if normalized_channel not in {item.value for item in OutboundDeliveryChannel}:
            raise OutboundWebhookValidationError(
                f"Unsupported delivery channel: {normalized_channel}"
            )
        query = (
            select(OutboundWebhookDelivery)
            .options(
                selectinload(OutboundWebhookDelivery.event),
                selectinload(OutboundWebhookDelivery.target),
            )
            .where(
                OutboundWebhookDelivery.channel
                == normalized_channel
            )
        )
        if target_id is not None:
            query = query.where(OutboundWebhookDelivery.target_id == target_id)
        if status is not None:
            normalized_status = self._enum_value(status)
            if normalized_status not in {item.value for item in OutboundWebhookDeliveryStatus}:
                raise OutboundWebhookValidationError(f"Unsupported delivery status: {normalized_status}")
            query = query.where(OutboundWebhookDelivery.status == normalized_status)

        result = await self.db.execute(
            query.order_by(
                OutboundWebhookDelivery.created_at.desc(),
                OutboundWebhookDelivery.id.desc(),
            ).limit(limit)
        )
        return [self._delivery_response(delivery) for delivery in result.scalars().all()]

    def _retry_delay_seconds(self, attempt_count: int) -> int:
        """Return capped exponential delay after one failed attempt."""
        exponent = max(attempt_count - 1, 0)
        return min(self.retry_max_seconds, self.retry_base_seconds * (2**exponent))

    def _webhook_delivery(
        self,
        event: OutboundWebhookEvent,
        target: OutboundWebhookTarget,
        *,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    ) -> OutboundWebhookDelivery:
        """Snapshot one webhook target into a durable queue row."""
        return OutboundWebhookDelivery(
            target_id=target.id,
            event_id=event.id,
            target_name=target.name,
            target_url=target.url,
            channel=OutboundDeliveryChannel.WEBHOOK.value,
            payload_json={
                "headers": self._json_safe(target.headers_json or {}),
                "secret": target.secret,
            },
            max_attempts=max_attempts,
        )

    def _email_delivery(
        self,
        event: OutboundWebhookEvent,
        payload: dict[str, Any],
    ) -> OutboundWebhookDelivery:
        """Create a status-email intent consumed by the same durable worker."""
        recipients = [
            email
            for email in (
                payload.get("manager_email"),
                payload.get("assignee_email"),
            )
            if email
        ]
        return OutboundWebhookDelivery(
            target_id=None,
            event_id=event.id,
            target_name=", ".join(recipients),
            target_url="smtp://runtime-settings",
            channel=OutboundDeliveryChannel.EMAIL.value,
            payload_json=self._json_safe(payload),
            max_attempts=DEFAULT_MAX_ATTEMPTS,
        )

    async def _enqueue_event_records(
        self,
        *,
        event_type: str,
        entity_type: str,
        entity_id: Optional[int],
        data: dict[str, Any],
        explicit_target: Optional[OutboundWebhookTarget] = None,
        email_payload: Optional[dict[str, Any]] = None,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        commit: bool = True,
    ) -> tuple[OutboundWebhookEvent, list[OutboundWebhookDelivery], bool]:
        """Persist an event and every matching transport intent without I/O."""
        event_type = event_type.strip()
        entity_type = entity_type.strip()
        if not event_type or "." not in event_type:
            raise OutboundWebhookValidationError("event_type must use dot notation")
        if not entity_type:
            raise OutboundWebhookValidationError("entity_type is required")

        event = OutboundWebhookEvent(
            event_id=uuid4().hex,
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            payload_json=self._json_safe(data or {}),
        )
        self.db.add(event)
        await self.db.flush()

        if explicit_target is not None:
            targets = [explicit_target]
        else:
            targets = [
                target
                for target in await self._enabled_targets()
                if self._event_matches(
                    event_type,
                    target.subscribed_events_json or [],
                )
            ]

        deliveries = [
            self._webhook_delivery(
                event,
                target,
                max_attempts=max_attempts,
            )
            for target in targets
        ]
        email_queued = False
        if email_payload is not None:
            recipients = [
                email_payload.get("manager_email"),
                email_payload.get("assignee_email"),
            ]
            try:
                settings = await EmailSettingsService(self.db).get_settings()
            except Exception:
                # Invalid optional SMTP configuration must not fail the task
                # transaction; the skipped intent is observable in server logs.
                logger.warning(
                    "Unable to resolve email settings while enqueueing status delivery",
                    exc_info=True,
                    extra={"entity_id": entity_id, "event_type": event_type},
                )
            else:
                if settings.is_configured and any(recipients):
                    deliveries.append(self._email_delivery(event, email_payload))
                    email_queued = True

        self.db.add_all(deliveries)
        await self.db.flush()
        for delivery in deliveries:
            delivery.event = event
        if commit:
            await self.db.commit()
        return event, deliveries, email_queued

    async def enqueue_event(
        self,
        *,
        event_type: str,
        entity_type: str,
        entity_id: Optional[int],
        data: dict[str, Any],
        commit: bool = True,
    ) -> Optional[OutboundWebhookEvent]:
        """Persist webhook intents; a worker performs external I/O later."""
        event, _, _ = await self._enqueue_event_records(
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            data=data,
            commit=commit,
        )
        return event

    async def enqueue_status_change(
        self,
        *,
        event_type: str,
        entity_type: str,
        entity_id: Optional[int],
        data: dict[str, Any],
        email_payload: dict[str, Any],
        commit: bool = False,
    ) -> bool:
        """Atomically enqueue status webhooks and the optional email intent."""
        _, _, email_queued = await self._enqueue_event_records(
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            data=data,
            email_payload=email_payload,
            commit=commit,
        )
        return email_queued

    async def emit_event(
        self,
        *,
        event_type: str,
        entity_type: str,
        entity_id: Optional[int],
        data: dict[str, Any],
    ) -> Optional[OutboundWebhookEvent]:
        """Backward-compatible enqueue-only event entry point."""
        return await self.enqueue_event(
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            data=data,
        )

    async def safe_emit_event(
        self,
        *,
        event_type: str,
        entity_type: str,
        entity_id: Optional[int],
        data: dict[str, Any],
        commit: bool = True,
    ) -> None:
        """Compatibility wrapper that propagates local persistence failures."""
        await self.enqueue_event(
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            data=data,
            commit=commit,
        )

    async def _attempt_webhook(self, delivery: OutboundWebhookDelivery) -> None:
        """Perform one webhook request using the configuration snapshot."""
        payload = self._delivery_payload(delivery.event)
        body = self._body_bytes(payload)
        config = delivery.payload_json or {}
        headers = {
            **(config.get("headers") or {}),
            "Content-Type": "application/json",
            "X-WorkChord-Event": delivery.event.event_type,
            "X-WorkChord-Event-Id": delivery.event.event_id,
            "X-WorkChord-Delivery-Id": str(delivery.id),
        }
        if config.get("secret"):
            headers["X-WorkChord-Signature-256"] = self._signature_header(
                config["secret"],
                body,
            )

        client_kwargs: dict[str, Any] = {"timeout": self.timeout_seconds}
        if self.transport is not None:
            client_kwargs["transport"] = self.transport
        try:
            normalize_external_http_url(
                delivery.target_url,
                resolve=self.transport is None,
            )
        except URLPolicyError as exc:
            raise OutboundDeliveryAttemptError(str(exc), retryable=False) from exc

        async with httpx.AsyncClient(**client_kwargs) as client:
            response = await client.post(
                delivery.target_url,
                content=body,
                headers=headers,
            )
        delivery.last_http_status = response.status_code
        delivery.last_response_body = response.text[:MAX_RESPONSE_BODY_LENGTH]
        if 200 <= response.status_code < 300:
            return
        retryable = response.status_code in {408, 429} or response.status_code >= 500
        raise OutboundDeliveryAttemptError(
            f"HTTP {response.status_code}",
            retryable=retryable,
        )

    async def _attempt_email(self, delivery: OutboundWebhookDelivery) -> None:
        """Perform one status email through the existing notification renderer."""
        sent = await self.notification_service.notify_status_change(
            **(delivery.payload_json or {})
        )
        if not sent:
            raise OutboundDeliveryAttemptError(
                "SMTP notification was not sent",
                retryable=True,
            )

    async def _attempt_delivery(
        self,
        delivery: OutboundWebhookDelivery,
        *,
        now: Optional[datetime] = None,
    ) -> None:
        """Attempt one claimed delivery and persist success, retry, or terminal state."""
        attempted_at = as_utc(now) if now is not None else utc_now()
        delivery.attempt_count += 1
        delivery.last_attempt_at = attempted_at
        delivery.last_http_status = None
        delivery.last_error = None
        delivery.last_response_body = None
        try:
            if delivery.channel == OutboundDeliveryChannel.WEBHOOK.value:
                await self._attempt_webhook(delivery)
            elif delivery.channel == OutboundDeliveryChannel.EMAIL.value:
                await self._attempt_email(delivery)
            else:
                raise OutboundDeliveryAttemptError(
                    f"Unsupported delivery channel: {delivery.channel}",
                    retryable=False,
                )
        except Exception as exc:
            # External HTTP and SMTP failures are isolated per durable job. The
            # worker records bounded retry state instead of failing the mutation.
            retryable = (
                exc.retryable
                if isinstance(exc, OutboundDeliveryAttemptError)
                else True
            )
            delivery.last_error = str(exc)[:MAX_RESPONSE_BODY_LENGTH]
            if retryable and delivery.attempt_count < delivery.max_attempts:
                delivery.status = OutboundWebhookDeliveryStatus.PENDING.value
                delivery.next_retry_at = attempted_at + timedelta(
                    seconds=self._retry_delay_seconds(delivery.attempt_count)
                )
                delivery.terminal_at = None
            else:
                delivery.status = OutboundWebhookDeliveryStatus.FAILED.value
                delivery.next_retry_at = None
                delivery.terminal_at = attempted_at
            logger.warning(
                "Outbound delivery attempt failed",
                exc_info=True,
                extra={
                    "delivery_id": delivery.id,
                    "channel": delivery.channel,
                    "attempt_count": delivery.attempt_count,
                    "terminal": delivery.status
                    == OutboundWebhookDeliveryStatus.FAILED.value,
                },
            )
        else:
            delivery.status = OutboundWebhookDeliveryStatus.DELIVERED.value
            delivery.delivered_at = attempted_at
            delivery.next_retry_at = None
            delivery.terminal_at = None
        finally:
            delivery.lease_token = None
            delivery.lease_expires_at = None
        await self.db.commit()

    def _claim_conditions(
        self,
        now: datetime,
    ) -> tuple[Any, ...]:
        return (
            OutboundWebhookDelivery.status
            == OutboundWebhookDeliveryStatus.PENDING.value,
            OutboundWebhookDelivery.attempt_count
            < OutboundWebhookDelivery.max_attempts,
            or_(
                OutboundWebhookDelivery.next_retry_at.is_(None),
                OutboundWebhookDelivery.next_retry_at <= now,
            ),
            or_(
                OutboundWebhookDelivery.lease_expires_at.is_(None),
                OutboundWebhookDelivery.lease_expires_at <= now,
            ),
        )

    async def _claim_delivery_id(
        self,
        delivery_id: int,
        *,
        worker_id: str,
        now: datetime,
        require_due: bool = True,
    ) -> Optional[str]:
        """Claim one row through a compare-and-set update."""
        lease_token = self._lease_token(worker_id)
        statement = update(OutboundWebhookDelivery).where(
            OutboundWebhookDelivery.id == delivery_id,
            OutboundWebhookDelivery.status
            == OutboundWebhookDeliveryStatus.PENDING.value,
        )
        if require_due:
            statement = statement.where(*self._claim_conditions(now))
        else:
            statement = statement.where(
                or_(
                    OutboundWebhookDelivery.lease_expires_at.is_(None),
                    OutboundWebhookDelivery.lease_expires_at <= now,
                )
            )
        statement = (
            statement.values(
                lease_token=lease_token,
                lease_expires_at=now + timedelta(seconds=self.lease_seconds),
            )
            .returning(OutboundWebhookDelivery.id)
            .execution_options(synchronize_session=False)
        )
        async def claim_once(_attempt: int) -> Optional[str]:
            result = await self.db.execute(statement)
            claimed = result.scalar_one_or_none()
            await self.db.commit()
            return lease_token if claimed is not None else None

        return await run_database_retry(
            claim_once,
            operation_name="outbound_delivery_claim",
            safe_to_retry=True,
            rollback=self.db.rollback,
        )

    async def _claim_due_postgresql(
        self,
        *,
        limit: int,
        worker_id: str,
        now: datetime,
    ) -> list[tuple[int, str]]:
        """Claim one fair PostgreSQL batch under SKIP LOCKED row locks."""

        async def claim_batch(_attempt: int) -> list[tuple[int, str]]:
            result = await self.db.execute(
                select(OutboundWebhookDelivery.id)
                .where(*self._claim_conditions(now))
                .order_by(
                    OutboundWebhookDelivery.next_retry_at.asc().nulls_first(),
                    OutboundWebhookDelivery.created_at.asc().nulls_last(),
                    OutboundWebhookDelivery.id.asc(),
                )
                .limit(limit)
                .with_for_update(skip_locked=True)
            )
            claimed: list[tuple[int, str]] = []
            for delivery_id in result.scalars().all():
                lease_token = self._lease_token(worker_id)
                await self.db.execute(
                    update(OutboundWebhookDelivery)
                    .where(OutboundWebhookDelivery.id == delivery_id)
                    .values(
                        lease_token=lease_token,
                        lease_expires_at=now + timedelta(seconds=self.lease_seconds),
                    )
                    .execution_options(synchronize_session=False)
                )
                claimed.append((delivery_id, lease_token))
            await self.db.commit()
            return claimed

        return await run_database_retry(
            claim_batch,
            operation_name="outbound_delivery_claim_batch",
            safe_to_retry=True,
            rollback=self.db.rollback,
        )

    async def claim_due_deliveries(
        self,
        *,
        limit: int = 50,
        worker_id: Optional[str] = None,
        now: Optional[datetime] = None,
    ) -> list[tuple[int, str]]:
        """Claim due rows so concurrent workers cannot send the same attempt."""
        claimed_at = as_utc(now) if now is not None else utc_now()
        worker = worker_id or f"worker-{uuid4().hex}"
        if self.db.get_bind().dialect.name == "postgresql":
            return await self._claim_due_postgresql(
                limit=limit,
                worker_id=worker,
                now=claimed_at,
            )
        result = await self.db.execute(
            select(OutboundWebhookDelivery.id)
            .where(*self._claim_conditions(claimed_at))
            .order_by(
                OutboundWebhookDelivery.next_retry_at.asc().nulls_first(),
                OutboundWebhookDelivery.created_at.asc().nulls_last(),
                OutboundWebhookDelivery.id.asc(),
            )
            .limit(limit)
        )
        claimed: list[tuple[int, str]] = []
        for delivery_id in result.scalars().all():
            token = await self._claim_delivery_id(
                delivery_id,
                worker_id=worker,
                now=claimed_at,
            )
            if token is not None:
                claimed.append((delivery_id, token))
        return claimed

    async def process_claimed_delivery(
        self,
        delivery_id: int,
        lease_token: str,
        *,
        now: Optional[datetime] = None,
    ) -> bool:
        """Perform external I/O only for the worker holding the current lease."""
        result = await self.db.execute(
            select(OutboundWebhookDelivery)
            .options(
                selectinload(OutboundWebhookDelivery.event),
                selectinload(OutboundWebhookDelivery.target),
            )
            .where(
                OutboundWebhookDelivery.id == delivery_id,
                OutboundWebhookDelivery.lease_token == lease_token,
            )
            .execution_options(populate_existing=True)
        )
        delivery = result.scalar_one_or_none()
        if delivery is None:
            await self.db.rollback()
            return False
        await self.db.commit()
        await self._attempt_delivery(delivery, now=now)
        return True

    async def run_due_jobs(
        self,
        *,
        limit: int = 50,
        worker_id: Optional[str] = None,
        now: Optional[datetime] = None,
    ) -> int:
        """Claim and process one bounded batch with per-target isolation."""
        claimed = await self.claim_due_deliveries(
            limit=limit,
            worker_id=worker_id,
            now=now,
        )
        completed = 0
        for delivery_id, lease_token in claimed:
            activity.worker_job_started()
            success = False
            try:
                processed = await self.process_claimed_delivery(
                    delivery_id,
                    lease_token,
                    now=now,
                )
                success = bool(processed)
            except Exception:
                # A database/process failure is isolated to one claimed row; its
                # lease expiry makes it recoverable by a restarted worker.
                logger.error(
                    "Outbound worker could not finalize claimed delivery",
                    exc_info=True,
                    extra={"delivery_id": delivery_id},
                )
                await self.db.rollback()
                metrics.increment(
                    "workchord_delivery_worker_jobs_total",
                    labels={"outcome": "failed"},
                )
                continue
            finally:
                activity.worker_job_finished(success=success)
            completed += int(success)
            metrics.increment(
                "workchord_delivery_worker_jobs_total",
                labels={"outcome": "processed" if success else "lease_lost"},
            )
        return completed

    async def test_target(self, target_id: int) -> Optional[OutboundWebhookRetryResponse]:
        """Enqueue and immediately process one test delivery."""
        target = await self.get_target(target_id)
        if target is None:
            return None
        _, deliveries, _ = await self._enqueue_event_records(
            event_type="webhook.test",
            entity_type="webhook_target",
            entity_id=target.id,
            data={"target_id": target.id, "target_name": target.name},
            explicit_target=target,
            max_attempts=1,
        )
        delivery = deliveries[0]
        token = await self._claim_delivery_id(
            delivery.id,
            worker_id="manual-test",
            now=utc_now(),
        )
        if token is None:
            raise OutboundWebhookNotFoundError("Test delivery could not be claimed")
        await self.process_claimed_delivery(delivery.id, token)
        loaded = await self._load_delivery(delivery.id)
        return (
            OutboundWebhookRetryResponse(delivery=self._delivery_response(loaded))
            if loaded is not None
            else None
        )

    async def retry_delivery(self, delivery_id: int) -> Optional[OutboundWebhookRetryResponse]:
        """Request and immediately process one manual outbound retry."""
        delivery = await self._load_delivery(delivery_id)
        if delivery is None:
            return None
        if delivery.channel == OutboundDeliveryChannel.WEBHOOK.value:
            if delivery.target is None:
                raise OutboundWebhookValidationError(
                    "Cannot retry delivery because its target was deleted"
                )
            delivery.target_url = delivery.target.url
            delivery.target_name = delivery.target.name
            delivery.payload_json = {
                "headers": self._json_safe(delivery.target.headers_json or {}),
                "secret": delivery.target.secret,
            }
        elif delivery.channel != OutboundDeliveryChannel.EMAIL.value:
            raise OutboundWebhookValidationError(
                f"Unsupported delivery channel: {delivery.channel}"
            )
        delivery.status = OutboundWebhookDeliveryStatus.PENDING.value
        delivery.next_retry_at = utc_now()
        delivery.terminal_at = None
        delivery.delivered_at = None
        delivery.max_attempts = max(
            delivery.max_attempts,
            delivery.attempt_count + 1,
        )
        delivery.lease_token = None
        delivery.lease_expires_at = None
        await self.db.commit()

        token = await self._claim_delivery_id(
            delivery.id,
            worker_id="manual-retry",
            now=utc_now(),
        )
        if token is None:
            raise OutboundWebhookNotFoundError("Delivery could not be claimed for retry")
        await self.process_claimed_delivery(delivery.id, token)
        loaded = await self._load_delivery(delivery.id)
        return (
            OutboundWebhookRetryResponse(delivery=self._delivery_response(loaded))
            if loaded is not None
            else None
        )


async def run_due_outbound_delivery_jobs(
    *,
    limit: int = 50,
    worker_id: Optional[str] = None,
) -> int:
    """Callable one-shot entry point for embedded or external workers."""
    from app.database import async_session_maker

    require_background_writes_enabled("outbound delivery worker")
    async with async_session_maker() as db:
        return await OutboundWebhookService(db).run_due_jobs(
            limit=limit,
            worker_id=worker_id,
        )


async def outbound_delivery_worker_loop(
    stop_event: asyncio.Event,
    *,
    poll_seconds: float = 1.0,
    batch_size: int = 50,
) -> None:
    """Poll durable outbound jobs until application shutdown."""
    require_background_writes_enabled("outbound delivery worker")
    activity.worker_started()
    try:
        while not stop_event.is_set():
            try:
                await run_due_outbound_delivery_jobs(limit=batch_size)
            except Exception:
                # The process boundary stays alive after a transient database error;
                # claimed rows become available when their leases expire.
                logger.error("Outbound delivery worker iteration failed", exc_info=True)
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=poll_seconds)
            except TimeoutError:
                continue
    finally:
        activity.worker_stopped()


async def emit_outbound_webhook_event(
    db: AsyncSession,
    *,
    event_type: str,
    entity_type: str,
    entity_id: Optional[int],
    data: dict[str, Any],
    commit: bool = True,
) -> None:
    """Persist or stage a domain event without external provider I/O."""
    await OutboundWebhookService(db).safe_emit_event(
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        data=data,
        commit=commit,
    )
