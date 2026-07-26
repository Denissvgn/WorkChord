"""Fail-closed maintenance/validation authority shared by REST, MCP, and workers."""

from __future__ import annotations

import hashlib
import json
import re
import socket
from time import monotonic
from typing import Any
from uuid import uuid4

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.config import get_settings
from app.runtime_telemetry import activity, correlation_id_context, metrics


SAFE_HTTP_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})
MCP_PATH_SUFFIXES = ("/mcp", "/mcp/")
_CORRELATION_ID_PATTERN = re.compile(r"[A-Za-z0-9_.:-]{1,128}")


class MaintenanceModeError(RuntimeError):
    """A write or non-allowlisted validation read was fenced."""

    def __init__(self, *, operation: str, mode: str):
        self.operation = operation
        self.mode = mode
        super().__init__(f"{operation} is unavailable while mode is {mode}")

    def detail(self) -> dict[str, Any]:
        settings = get_settings()
        return {
            "code": "maintenance_mode",
            "message": str(self),
            "mode": self.mode,
            "retry_after_seconds": settings.maintenance_retry_after_seconds,
        }


def maintenance_configuration_fingerprint() -> str:
    """Identify the complete restart-bound fence configuration."""

    settings = get_settings()
    payload = {
        "allowlist": settings.maintenance_validation_allowlist,
        "mode": settings.maintenance_mode,
        "revision": settings.maintenance_revision,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def maintenance_state() -> dict[str, Any]:
    settings = get_settings()
    replica_id = (
        socket.gethostname()
        if settings.maintenance_replica_id == "auto"
        else settings.maintenance_replica_id
    )
    return {
        "mode": settings.maintenance_mode,
        "accepts_writes": settings.maintenance_mode == "off",
        "revision": settings.maintenance_revision,
        "replica_id": replica_id,
        "configuration_fingerprint": maintenance_configuration_fingerprint(),
        "validation_allowlist": list(settings.maintenance_validation_allowlist),
    }


def _path_allowed(path: str, allowlist: list[str]) -> bool:
    normalized = path.rstrip("/") or "/"
    for entry in allowlist:
        if entry.endswith("/*"):
            prefix = entry[:-2].rstrip("/")
            if normalized == prefix or normalized.startswith(prefix + "/"):
                return True
        elif normalized == entry:
            return True
    return False


def _is_mcp_path(path: str) -> bool:
    normalized = path.rstrip("/")
    return any(normalized.endswith(suffix.rstrip("/")) for suffix in MCP_PATH_SUFFIXES)


def scope_requirement_is_mutating(required_scope: Any) -> bool:
    """Classify MCP mutations from their enforced authorization contract.

    Read tools sometimes accept a write scope as an alternative.  Such a tuple
    also contains an explicit read scope, so only write-only/execute-only
    requirements are classified as mutations.
    """

    if required_scope is None:
        return False
    scopes = (required_scope,) if isinstance(required_scope, str) else tuple(required_scope)
    has_read = any(scope.endswith(":read") for scope in scopes)
    has_write = any(
        scope.endswith(":write") or scope.endswith(":execute")
        for scope in scopes
    )
    return has_write and not has_read


def enforce_mcp_access(required_scope: Any) -> None:
    """Fence every scope-classified MCP mutation before opening a transaction."""

    mode = get_settings().maintenance_mode
    if mode == "off" or not scope_requirement_is_mutating(required_scope):
        return
    raise MaintenanceModeError(operation="MCP mutation", mode=mode)


def require_background_writes_enabled(operation: str) -> None:
    """Fence worker, seed, and repair writes under the same deployment mode."""

    mode = get_settings().maintenance_mode
    if mode != "off":
        raise MaintenanceModeError(operation=operation, mode=mode)


def _header(scope: Scope, name: str) -> str | None:
    target = name.lower().encode("latin1")
    for key, value in scope.get("headers", []):
        if key.lower() == target:
            return value.decode("latin1")
    return None


class RuntimeBoundaryMiddleware:
    """Enforce REST fencing and record bounded request/drain telemetry."""

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        settings = get_settings()
        method = str(scope.get("method", "GET")).upper()
        path = str(scope.get("path", "/"))
        mutation = method not in SAFE_HTTP_METHODS
        mode = settings.maintenance_mode

        allowed = True
        if mode != "off" and mutation and not _is_mcp_path(path):
            allowed = False
        elif (
            mode == "validation-only"
            and not _is_mcp_path(path)
            and not _path_allowed(path, settings.maintenance_validation_allowlist)
        ):
            allowed = False

        if not allowed:
            error = MaintenanceModeError(
                operation=f"{method} {path}",
                mode=mode,
            )
            response = JSONResponse(
                status_code=503,
                content={"detail": error.detail()},
                headers={
                    "Retry-After": str(settings.maintenance_retry_after_seconds),
                    "Cache-Control": "no-store",
                },
            )
            await response(scope, receive, send)
            metrics.increment(
                "workchord_maintenance_rejections_total",
                labels={"surface": "rest"},
            )
            return

        supplied_correlation_id = _header(scope, "x-correlation-id") or ""
        correlation_id = (
            supplied_correlation_id
            if _CORRELATION_ID_PATTERN.fullmatch(supplied_correlation_id)
            else uuid4().hex
        )
        token = correlation_id_context.set(correlation_id)
        activity.begin_request(mutation=mutation and not _is_mcp_path(path))
        started = monotonic()
        status_code = 500

        async def send_with_metrics(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = int(message["status"])
                headers = list(message.get("headers", []))
                headers.append((b"x-correlation-id", correlation_id.encode("ascii")))
                message = {**message, "headers": headers}
            await send(message)

        try:
            await self.app(scope, receive, send_with_metrics)
        finally:
            elapsed = monotonic() - started
            activity.end_request(mutation=mutation and not _is_mcp_path(path))
            metrics.increment(
                "workchord_http_requests_total",
                labels={"method": method, "status_class": f"{status_code // 100}xx"},
            )
            metrics.observe(
                "workchord_http_request_duration_seconds",
                elapsed,
                labels={"method": method},
            )
            correlation_id_context.reset(token)
