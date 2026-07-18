"""DBM-PERF-002 and DBM-MAINT-001 runtime-boundary tests."""

from __future__ import annotations

import ast
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.routing import APIRoute
import pytest

from app.config import get_settings
from app.maintenance import (
    MaintenanceModeError,
    RuntimeBoundaryMiddleware,
    enforce_mcp_access,
    scope_requirement_is_mutating,
)
from app.models.user_session import UserSession
from app.models.agent import AgentActor
from app.services.agent_service import AgentService, hash_api_key
from app.services.email_settings_service import EmailSettings
from app.services.notification_service import NotificationService
from app.services.session_service import _token_digest, get_or_create_session


@pytest.fixture(autouse=True)
def clear_runtime_settings_cache() -> Any:
    yield
    get_settings.cache_clear()


class ScalarResult:
    def __init__(self, value: Any):
        self.value = value

    def scalar_one_or_none(self) -> Any:
        return self.value


class SessionDouble:
    def __init__(self, resolved_session: UserSession | None):
        self.resolved_session = resolved_session
        self.commits = 0
        self.refreshes = 0

    async def execute(self, _statement: Any) -> ScalarResult:
        return ScalarResult(self.resolved_session)

    async def commit(self) -> None:
        self.commits += 1

    async def refresh(self, _instance: Any) -> None:
        self.refreshes += 1


def _configure_mode(monkeypatch: pytest.MonkeyPatch, mode: str) -> None:
    monkeypatch.setenv("DEPLOYMENT_ENVIRONMENT", "test")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    monkeypatch.setenv("DATABASE_SSL_MODE", "disable")
    monkeypatch.setenv("MAINTENANCE_MODE", mode)
    monkeypatch.setenv("MAINTENANCE_REVISION", "runtime-boundary-test")
    monkeypatch.setenv("MAINTENANCE_REPLICA_ID", "replica-test")
    monkeypatch.setenv(
        "MAINTENANCE_VALIDATION_ALLOWLIST",
        json.dumps(["/health/live", "/health/ready", "/metrics"]),
    )
    get_settings.cache_clear()


async def _asgi_request(app: Any, method: str, path: str) -> tuple[int, dict[str, str], bytes]:
    sent: list[dict[str, Any]] = []
    received = False

    async def receive() -> dict[str, Any]:
        nonlocal received
        if received:
            return {"type": "http.disconnect"}
        received = True
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: dict[str, Any]) -> None:
        sent.append(message)

    await app(
        {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": method,
            "scheme": "http",
            "path": path,
            "raw_path": path.encode("ascii"),
            "query_string": b"",
            "headers": [],
            "client": ("127.0.0.1", 1234),
            "server": ("testserver", 80),
        },
        receive,
        send,
    )
    start = next(message for message in sent if message["type"] == "http.response.start")
    headers = {
        key.decode("latin1"): value.decode("latin1")
        for key, value in start.get("headers", [])
    }
    body = b"".join(
        message.get("body", b"")
        for message in sent
        if message["type"] == "http.response.body"
    )
    return int(start["status"]), headers, body


def _boundary_app() -> FastAPI:
    app = FastAPI()

    @app.get("/health/live")
    async def live() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/read")
    async def read() -> dict[str, str]:
        return {"status": "read"}

    @app.post("/api/new-unclassified-mutation")
    async def new_mutation() -> dict[str, str]:
        return {"status": "mutated"}

    app.add_middleware(RuntimeBoundaryMiddleware)
    return app


@pytest.mark.asyncio
async def test_validation_only_is_exact_allowlist_and_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _configure_mode(monkeypatch, "validation-only")
    app = _boundary_app()

    live_status, live_headers, _ = await _asgi_request(app, "GET", "/health/live")
    read_status, _, read_body = await _asgi_request(app, "GET", "/api/read")
    write_status, write_headers, write_body = await _asgi_request(
        app,
        "POST",
        "/api/new-unclassified-mutation",
    )

    assert live_status == 200
    assert "x-correlation-id" in live_headers
    assert read_status == 503
    assert json.loads(read_body)["detail"]["code"] == "maintenance_mode"
    assert write_status == 503
    assert write_headers["retry-after"] == "60"
    assert json.loads(write_body)["detail"]["mode"] == "validation-only"


@pytest.mark.asyncio
async def test_read_only_maintenance_allows_reads_but_rejects_every_new_write(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _configure_mode(monkeypatch, "read-only-maintenance")
    app = _boundary_app()

    assert (await _asgi_request(app, "GET", "/api/read"))[0] == 200
    assert (
        await _asgi_request(app, "POST", "/api/new-unclassified-mutation")
    )[0] == 503


def test_mcp_scope_contract_fences_mutations_and_preserves_read_tools(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _configure_mode(monkeypatch, "validation-only")

    assert scope_requirement_is_mutating("tasks:write") is True
    assert scope_requirement_is_mutating("work:execute") is True
    assert scope_requirement_is_mutating(("tasks:read", "tasks:write")) is False
    enforce_mcp_access("tasks:read")
    enforce_mcp_access(("tasks:read", "tasks:write"))
    with pytest.raises(MaintenanceModeError):
        enforce_mcp_access("new_resource:write")


def test_application_has_one_fail_closed_boundary_for_all_rest_mutations() -> None:
    from app.main import app

    boundary_types = {middleware.cls for middleware in app.user_middleware}
    assert RuntimeBoundaryMiddleware in boundary_types

    mutation_routes: set[tuple[str, str]] = set()
    for included in app.routes:
        original_router = getattr(included, "original_router", None)
        if original_router is None:
            candidates = [included]
            prefix = ""
        else:
            candidates = original_router.routes
            prefix = included.include_context.prefix
        for route in candidates:
            if not isinstance(route, APIRoute):
                continue
            mutation_routes.update(
                (f"{prefix}{route.path}", method)
                for method in route.methods
                if method not in {"GET", "HEAD", "OPTIONS"}
            )
    assert len(mutation_routes) >= 50
    assert ("/api/session/rotate", "POST") in mutation_routes
    assert any(path.endswith("/import") for path, _method in mutation_routes)
    assert any("agent" in path for path, _method in mutation_routes)


def test_every_mcp_tool_uses_scope_classification_and_mutators_are_write_only() -> None:
    source_path = Path(__file__).resolve().parents[1] / "app/mcp_server.py"
    module = ast.parse(source_path.read_text(encoding="utf-8"))
    mutation_prefixes = (
        "create_",
        "update_",
        "delete_",
        "begin_",
        "renew_",
        "report_",
        "submit_",
        "fail_",
        "requeue_",
        "claim_",
        "release_",
        "patch_",
        "append_",
        "start_",
        "finish_",
        "accept_",
        "decline_",
        "snooze_",
        "mark_",
        "convert_",
        "add_",
        "apply_",
        "reorder_",
        "import_",
        "ship_",
        "link_",
        "unlink_",
        "retry_",
        "rotate_",
        "provision_",
        "set_",
    )
    tools_checked = 0
    for node in ast.walk(module):
        if not isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
            continue
        is_tool = any(
            isinstance(decorator, ast.Call)
            and isinstance(decorator.func, ast.Attribute)
            and decorator.func.attr == "tool"
            for decorator in node.decorator_list
        )
        if not is_tool:
            continue
        tools_checked += 1
        calls = [
            call
            for call in ast.walk(node)
            if isinstance(call, ast.Call)
            and isinstance(call.func, ast.Name)
            and call.func.id == "_tool_call"
        ]
        assert len(calls) == 1, f"{node.name} must use exactly one _tool_call boundary"

        scope_node = calls[0].args[0]
        try:
            scope = ast.literal_eval(scope_node)
        except (ValueError, TypeError):
            scope = None  # Dynamic skill-catalog scope is read-only by contract.
        scopes = (scope,) if isinstance(scope, str) else scope or ()
        mutating = scope_requirement_is_mutating(scopes)
        semantic_name = node.name.removeprefix("agent_")
        if semantic_name.startswith(mutation_prefixes):
            assert mutating, f"{node.name} is an unclassified MCP mutation"

    assert tools_checked >= 80


@pytest.mark.asyncio
async def test_active_browser_reads_skip_session_commits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _configure_mode(monkeypatch, "off")
    token = "a" * 43
    session = UserSession(
        id=1,
        public_id="sessiontest1",
        session_token_hash=_token_digest(token),
        ip_address="192.0.2.10",
        user_agent="test-agent",
        last_seen_at=datetime.now(UTC),
        expires_at=datetime.now(UTC) + timedelta(hours=1),
    )
    db = SessionDouble(session)

    resolved, returned_token = await get_or_create_session(
        db,  # type: ignore[arg-type]
        "192.0.2.10",
        "test-agent",
        token,
    )

    assert resolved is session
    assert returned_token == token
    assert db.commits == 0
    assert db.refreshes == 0


@pytest.mark.asyncio
async def test_validation_session_resolution_has_no_hidden_touch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _configure_mode(monkeypatch, "validation-only")
    token = "b" * 43
    session = UserSession(
        id=2,
        public_id="sessiontest2",
        session_token_hash=_token_digest(token),
        ip_address="192.0.2.20",
        user_agent="old-agent",
        last_seen_at=datetime.now(UTC) - timedelta(days=1),
        expires_at=datetime.now(UTC) + timedelta(hours=1),
    )
    db = SessionDouble(session)

    resolved, _ = await get_or_create_session(
        db,  # type: ignore[arg-type]
        "192.0.2.99",
        "new-agent",
        token,
    )

    assert resolved is session
    assert db.commits == 0
    assert session.ip_address == "192.0.2.20"
    assert session.user_agent == "old-agent"


@pytest.mark.asyncio
async def test_validation_agent_authentication_has_no_hidden_last_seen_write(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _configure_mode(monkeypatch, "validation-only")
    api_key = "agent-secret"
    actor = AgentActor(
        id=1,
        name="validation-reader",
        display_name="Validation Reader",
        api_key_hash=hash_api_key(api_key),
        scopes='["tasks:read"]',
        last_seen_at=None,
    )
    db = SessionDouble(actor)  # type: ignore[arg-type]

    authenticated = await AgentService(db).authenticate(api_key)  # type: ignore[arg-type]

    assert authenticated is actor
    assert actor.last_seen_at is None
    assert db.commits == 0
    assert db.refreshes == 0


class ProviderSessionDouble:
    def __init__(self) -> None:
        self.checked_out = True
        self.commits = 0

    async def commit(self) -> None:
        self.commits += 1
        self.checked_out = False


@pytest.mark.asyncio
async def test_smtp_provider_wait_starts_after_database_release(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    db = ProviderSessionDouble()
    service = NotificationService(db)  # type: ignore[arg-type]

    async def settings() -> EmailSettings:
        return EmailSettings(
            enabled=True,
            smtp_host="smtp.example.test",
            smtp_from_email="workchord@example.test",
        )

    async def send(*_args: Any, **_kwargs: Any) -> None:
        # This stands in for an arbitrarily long provider wait.
        assert db.checked_out is False

    monkeypatch.setattr(service, "_settings", settings)
    monkeypatch.setattr("app.services.notification_service.aiosmtplib.send", send)

    assert await service.send_email(
        ["recipient@example.test"],
        "Subject",
        "<p>Body</p>",
    )
    assert db.commits == 1
