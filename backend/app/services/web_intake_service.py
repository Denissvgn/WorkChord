"""Controlled external web intake service."""
import hmac
import math
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.intake import WebIntakeRequest
from app.schemas.triage import TriageItemCreate
from app.services.triage_service import TriageService
from app.utils.time import utc_now


class WebIntakeConfigurationError(RuntimeError):
    """Raised when the intake endpoint is not configured."""


class WebIntakeUnauthorizedError(PermissionError):
    """Raised when an intake request is not authenticated."""


class WebIntakeRateLimitError(RuntimeError):
    """Raised when an intake requester exceeds the configured rate limit."""

    def __init__(self, retry_after_seconds: int, limit: int, client_ip: str):
        super().__init__("Web intake rate limit exceeded")
        self.retry_after_seconds = max(1, retry_after_seconds)
        self.limit = limit
        self.client_ip = client_ip
        self.window_seconds = 60
        self.reset_at = utc_now() + timedelta(seconds=self.retry_after_seconds)


@dataclass
class _RateLimitWindow:
    window_started_at: float
    count: int


class WebIntakeRateLimiter:
    """In-process fixed-window rate limiter keyed by client IP."""

    def __init__(
        self,
        window_seconds: int = 60,
        *,
        clock: Callable[[], float] = time.monotonic,
        max_entries: int = 10_000,
    ):
        self.window_seconds = window_seconds
        self.clock = clock
        self.max_entries = max(1, max_entries)
        self._windows: dict[str, _RateLimitWindow] = {}

    def _evict_expired(self, now: float) -> None:
        """Remove expired client windows without relying on wall-clock sleeps."""
        expired = [
            client
            for client, window in self._windows.items()
            if now - window.window_started_at >= self.window_seconds
        ]
        for client in expired:
            self._windows.pop(client, None)

    def _ensure_capacity(self, client_ip: str) -> None:
        """Cap active-cardinality memory while retaining the current client."""
        if client_ip in self._windows or len(self._windows) < self.max_entries:
            return
        oldest_client = min(
            self._windows,
            key=lambda client: self._windows[client].window_started_at,
        )
        self._windows.pop(oldest_client, None)

    def check(self, client_ip: str, limit: int) -> Optional[int]:
        """Return retry-after seconds when limited, otherwise allow the request."""
        normalized_limit = max(1, limit)
        now = self.clock()
        self._evict_expired(now)
        self._ensure_capacity(client_ip)
        window = self._windows.get(client_ip)
        if window is None or now - window.window_started_at >= self.window_seconds:
            self._windows[client_ip] = _RateLimitWindow(window_started_at=now, count=1)
            return None

        if window.count >= normalized_limit:
            return max(1, math.ceil(self.window_seconds - (now - window.window_started_at)))

        window.count += 1
        return None

    def reset(self) -> None:
        """Clear limiter state, primarily for tests."""
        self._windows.clear()


default_web_intake_rate_limiter = WebIntakeRateLimiter()


class WebIntakeService:
    """Validate controlled intake submissions and create triage items."""

    def __init__(
        self,
        db: AsyncSession,
        *,
        token: str,
        rate_limit_per_minute: int = 30,
        rate_limiter: WebIntakeRateLimiter = default_web_intake_rate_limiter,
    ):
        self.db = db
        self.token = token.strip() if token else ""
        self.rate_limit_per_minute = max(1, rate_limit_per_minute)
        self.rate_limiter = rate_limiter
        self.triage_service = TriageService(db)

    def verify_authorization(self, authorization_header: Optional[str]) -> None:
        """Validate configured bearer token auth."""
        if not self.token:
            raise WebIntakeConfigurationError("Web intake token is not configured")
        if not authorization_header or not authorization_header.startswith("Bearer "):
            raise WebIntakeUnauthorizedError("Missing web intake bearer token")

        supplied_token = authorization_header.removeprefix("Bearer ").strip()
        if not supplied_token or not hmac.compare_digest(supplied_token, self.token):
            raise WebIntakeUnauthorizedError("Invalid web intake bearer token")

    def check_rate_limit(self, client_ip: str) -> None:
        """Enforce the configured per-IP fixed-window limit."""
        retry_after = self.rate_limiter.check(client_ip, self.rate_limit_per_minute)
        if retry_after is not None:
            raise WebIntakeRateLimitError(retry_after, self.rate_limit_per_minute, client_ip)

    def _metadata(
        self,
        data: WebIntakeRequest,
        *,
        client_ip: str,
        user_agent: Optional[str],
    ) -> dict:
        """Merge caller metadata with trusted intake metadata."""
        metadata = dict(data.metadata_json or {})
        metadata["_web_intake"] = {
            "received_at": utc_now().isoformat(),
            "client_ip": client_ip,
            "user_agent": user_agent,
        }
        return metadata

    async def create_triage_item(
        self,
        data: WebIntakeRequest,
        *,
        authorization_header: Optional[str],
        client_ip: str,
        user_agent: Optional[str],
    ):
        """Authenticate, rate-limit, and create a triage item."""
        self.verify_authorization(authorization_header)
        self.check_rate_limit(client_ip)

        triage_data = TriageItemCreate(
            title=data.title,
            description=data.description,
            source=data.source,
            source_url=data.source_url,
            external_key=data.external_key,
            priority_hint=data.priority_hint,
            assignee_hint=data.assignee_hint,
            project_hint_id=data.project_hint_id,
            iteration_hint_id=data.iteration_hint_id,
            labels=data.labels,
            metadata_json=self._metadata(data, client_ip=client_ip, user_agent=user_agent),
        )
        return await self.triage_service.create(triage_data)
