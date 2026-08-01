"""MCP server facade for external LLM-agent integrations."""
import argparse
import asyncio
import json
import os
import sys
from contextlib import asynccontextmanager, redirect_stdout
from contextvars import ContextVar
from typing import Any, AsyncIterator, Callable, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from mcp.server.transport_security import TransportSecuritySettings
from pydantic import ValidationError as PydanticValidationError
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.types import ASGIApp, Receive, Scope, Send

from app import mcp_agent_tools
from app.config import get_settings
from app.database import async_session_maker, close_database, init_db
from app.maintenance import MaintenanceModeError, enforce_mcp_access
from app.models.agent import AgentActor
from app.services.agent_service import (
    AgentConflictError,
    AgentPermissionError,
    AgentService,
    actor_has_scope,
    require_scope,
)
from app.services.agent_model_catalog_service import AgentModelConflictError
from app.services.agent_routing_service import AgentRoutingConflictError
from app.services.agent_team_setup_service import AgentTeamSetupConflictError
from app.services.task_service import TaskVersionConflictError
from app.services.triage_service import TriageConflictError


MCP_AGENT_API_KEY_ENV = "MCP_AGENT_API_KEY"
_http_agent_key: ContextVar[Optional[str]] = ContextVar("mcp_http_agent_key", default=None)
_session_factory: Callable[[], Any] = async_session_maker


class MCPAuthError(PermissionError):
    """Raised when MCP agent authentication fails."""


def _mcp_transport_security_settings() -> TransportSecuritySettings:
    """Build the explicit Host/Origin allowlist shared by mounted and standalone MCP."""
    settings = get_settings()
    return TransportSecuritySettings(
        enable_dns_rebinding_protection=settings.mcp_dns_rebinding_protection,
        allowed_hosts=settings.mcp_allowed_hosts,
        allowed_origins=settings.mcp_allowed_origins,
    )


def _allowed_transport_value(value: str, allowed_values: list[str]) -> bool:
    if value in allowed_values:
        return True
    return any(
        allowed.endswith(":*") and value.startswith(f"{allowed[:-2]}:")
        for allowed in allowed_values
    )


class MCPHostValidationMiddleware:
    """Reject untrusted MCP Host/Origin values before database authentication."""

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        security = _mcp_transport_security_settings()
        if not security.enable_dns_rebinding_protection:
            await self.app(scope, receive, send)
            return
        headers = {
            key.decode("latin1").lower(): value.decode("latin1")
            for key, value in scope.get("headers", [])
        }
        host = headers.get("host", "")
        if not _allowed_transport_value(host, security.allowed_hosts):
            await PlainTextResponse("Invalid Host header", status_code=421)(
                scope, receive, send
            )
            return
        origin = headers.get("origin")
        if origin and not _allowed_transport_value(
            origin, security.allowed_origins
        ):
            await PlainTextResponse("Invalid Origin header", status_code=403)(
                scope, receive, send
            )
            return
        await self.app(scope, receive, send)


class MCPAgentKeyMiddleware:
    """Extract and validate MCP HTTP agent credentials before protocol handling."""

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        agent_key = _agent_key_from_scope(scope)
        if not agent_key:
            await PlainTextResponse("Missing MCP agent API key", status_code=401)(scope, receive, send)
            return

        try:
            async with _open_db_session() as db:
                await _authenticate_agent_key(db, agent_key)
        except MCPAuthError as exc:
            await PlainTextResponse(str(exc), status_code=401)(scope, receive, send)
            return

        token = _http_agent_key.set(agent_key)
        try:
            await self.app(scope, receive, send)
        finally:
            _http_agent_key.reset(token)


class MCPExactPathAlias:
    """Route exact MCP mount path requests into the Streamable HTTP root app."""

    def __init__(self, app: ASGIApp, mount_path: str):
        self.app = app
        self.mount_path = mount_path.rstrip("/")

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        rewritten = dict(scope)
        root_path = rewritten.get("root_path", "")
        rewritten["root_path"] = f"{root_path}{self.mount_path}"
        rewritten["path"] = "/"
        rewritten["raw_path"] = b"/"
        await self.app(rewritten, receive, send)


def set_mcp_session_factory(factory: Callable[[], Any]) -> None:
    """Override the DB session factory for tests."""
    global _session_factory
    _session_factory = factory


def reset_mcp_session_factory() -> None:
    """Restore the production DB session factory."""
    set_mcp_session_factory(async_session_maker)


@asynccontextmanager
async def _open_db_session() -> AsyncIterator[Any]:
    """Open a DB session from either production async factory or test override."""
    session_context = _session_factory()
    if hasattr(session_context, "__aenter__"):
        async with session_context as db:
            yield db
        return
    yield session_context


def _agent_key_from_scope(scope: Scope) -> Optional[str]:
    """Extract agent API key from HTTP MCP headers."""
    headers = {key.decode("latin1").lower(): value.decode("latin1") for key, value in scope.get("headers", [])}
    authorization = headers.get("authorization")
    if authorization and authorization.lower().startswith("bearer "):
        return authorization[7:].strip() or None
    return headers.get("x-agent-api-key")


def _current_agent_key() -> Optional[str]:
    """Return the HTTP or stdio MCP agent key."""
    return _http_agent_key.get() or os.getenv(MCP_AGENT_API_KEY_ENV)


async def _authenticate_agent_key(db: Any, api_key: str) -> AgentActor:
    """Authenticate a real agent actor and reject bootstrap execution."""
    settings = get_settings()
    if settings.agent_bootstrap_api_key and api_key == settings.agent_bootstrap_api_key:
        raise MCPAuthError("Bootstrap agent key cannot be used for MCP execution")

    actor = await AgentService(db).authenticate(api_key)
    if not actor:
        raise MCPAuthError("Invalid or disabled MCP agent API key")
    if actor.name == "bootstrap-agent":
        raise MCPAuthError("Bootstrap agent actor cannot be used for MCP execution")
    return actor


ScopeRequirement = Optional[str | tuple[str, ...]]
ROUTING_READ_SCOPE_REQUIREMENT: tuple[str, ...] = (
    "planning:read",
    "planning:write",
    "assignments:read",
    "assignments:write",
)


def _skill_bundle_scope_requirement() -> ScopeRequirement:
    """Match MCP skill delivery to the configured REST public/private mode."""
    return None if get_settings().agent_skill_bundles_public else "skills:read"


def _require_scope_requirement(actor: AgentActor, required: ScopeRequirement) -> None:
    """Require one scope or any scope from an explicit alternative set."""
    if required is None:
        return
    if isinstance(required, str):
        require_scope(actor, required)
        return
    if not any(actor_has_scope(actor, scope) for scope in required):
        raise AgentPermissionError(
            f"Missing required scope; expected one of: {', '.join(required)}"
        )


@asynccontextmanager
async def _agent_context(required_scope: ScopeRequirement = None) -> AsyncIterator[tuple[Any, AgentActor]]:
    """Open an authenticated MCP agent DB context."""
    api_key = _current_agent_key()
    if not api_key:
        raise MCPAuthError(f"Missing {MCP_AGENT_API_KEY_ENV} or HTTP agent key")
    async with _open_db_session() as db:
        actor = await _authenticate_agent_key(db, api_key)
        _require_scope_requirement(actor, required_scope)
        yield db, actor


def _structured_tool_error(exc: Exception) -> str:
    """Return stable, machine-readable conflict and validation errors."""
    if isinstance(exc, AgentRoutingConflictError):
        payload = exc.detail()
    elif isinstance(exc, AgentTeamSetupConflictError):
        payload = exc.detail()
    elif isinstance(exc, AgentModelConflictError):
        payload = exc.detail()
    elif isinstance(exc, TaskVersionConflictError):
        payload = exc.detail()
    elif isinstance(exc, AgentConflictError):
        payload = {"code": "agent_state_conflict", "message": str(exc)}
    elif isinstance(exc, TriageConflictError):
        payload = {"code": "triage_state_conflict", "message": str(exc)}
    elif isinstance(exc, AgentPermissionError):
        payload = {"code": "agent_permission_denied", "message": str(exc)}
    elif isinstance(exc, MCPAuthError):
        payload = {"code": "agent_authentication_failed", "message": str(exc)}
    elif isinstance(exc, MaintenanceModeError):
        payload = exc.detail()
    elif isinstance(exc, LookupError):
        payload = {"code": "agent_resource_not_found", "message": str(exc)}
    elif isinstance(exc, PydanticValidationError):
        payload = {
            "code": "agent_validation_error",
            "message": "Request validation failed",
            "errors": [
                {
                    "type": error.get("type", "value_error"),
                    "loc": list(error.get("loc", ())),
                }
                for error in exc.errors(include_url=False, include_context=False)
            ],
        }
    else:
        payload = {"code": "agent_validation_error", "message": str(exc)}
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)


async def _tool_call(required_scope: ScopeRequirement, func: Callable[[Any, AgentActor], Any]) -> Any:
    """Run a service-backed MCP tool and return MCP-safe errors."""
    try:
        enforce_mcp_access(required_scope)
        async with _agent_context(required_scope) as (db, actor):
            return await func(db, actor)
    except ToolError:
        raise
    except (
        MCPAuthError,
        MaintenanceModeError,
        AgentRoutingConflictError,
        AgentTeamSetupConflictError,
        AgentModelConflictError,
        AgentConflictError,
        AgentPermissionError,
        TriageConflictError,
        TaskVersionConflictError,
        ValueError,
        LookupError,
    ) as exc:
        raise ToolError(_structured_tool_error(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive redaction boundary
        raise ToolError("MCP tool failed") from exc


async def _json_resource(required_scope: ScopeRequirement, func: Callable[[Any, AgentActor], Any]) -> str:
    """Return a JSON resource payload through the authenticated MCP context."""
    value = await _tool_call(required_scope, func)
    return json.dumps(value, ensure_ascii=False, default=str)


async def _skill_bundle_prompt(value: str) -> str:
    """Authenticate and authorize one role prompt under bundle delivery policy."""
    async with _agent_context(_skill_bundle_scope_requirement()):
        return value


def create_mcp_server() -> FastMCP:
    """Create the WorkChord FastMCP server."""
    settings = get_settings()
    mcp = FastMCP(
        "WorkChord",
        instructions=(
            "Use these tools to inspect and execute WorkChord work. "
            "Stable workers first read capabilities and agent_get_my_work, then use "
            "agent_begin_my_work for the exact server-selected assignment. Include "
            "idempotency keys for every mutation. Legacy claim tools are supervised "
            "compatibility operations, not the assigned-work lifecycle."
        ),
        stateless_http=True,
        json_response=True,
        host=settings.mcp_http_host,
        streamable_http_path="/",
        transport_security=_mcp_transport_security_settings(),
    )

    @mcp.tool()
    async def agent_get_capabilities() -> dict[str, Any]:
        """Return authenticated actor identity, features, limits, and compatible skills."""
        return await _tool_call(
            None,
            lambda db, actor: mcp_agent_tools.get_agent_capabilities(db, actor),
        )

    @mcp.tool()
    async def agent_get_team_setup_status() -> dict[str, Any]:
        """Return desired, configured, and runtime readiness for the bound team."""
        return await _tool_call(
            ("planning:read", "admin"),
            lambda db, actor: mcp_agent_tools.get_agent_team_setup_status(
                db,
                actor,
            ),
        )

    @mcp.tool()
    async def agent_list_actor_roster(
        include_disabled: bool = False,
    ) -> list[dict[str, Any]]:
        """List enabled, secret-free actor dispatch metadata for PM routing."""
        return await _tool_call(
            ("assignments:read", "assignments:write", "planning:read"),
            lambda db, actor: mcp_agent_tools.list_agent_actor_roster(
                db,
                actor,
                include_disabled=include_disabled,
            ),
        )

    @mcp.tool()
    async def agent_list_model_catalog(
        include_disabled: bool = False,
    ) -> list[dict[str, Any]]:
        """List provider-neutral model capability declarations."""
        return await _tool_call(
            ("planning:read", "admin"),
            lambda db, actor: mcp_agent_tools.list_agent_model_catalog(
                db,
                actor,
                include_disabled=include_disabled,
            ),
        )

    @mcp.tool()
    async def agent_get_model_catalog_entry(
        catalog_key: str,
    ) -> dict[str, Any]:
        """Read one model capability declaration by stable key."""
        return await _tool_call(
            ("planning:read", "admin"),
            lambda db, actor: mcp_agent_tools.get_agent_model_catalog_entry(
                db,
                actor,
                catalog_key,
            ),
        )

    @mcp.tool()
    async def agent_list_model_bindings(
        actor_id: int | None = None,
        include_disabled: bool = False,
    ) -> list[dict[str, Any]]:
        """List secret-free actor model bindings."""
        return await _tool_call(
            ("planning:read", "admin"),
            lambda db, actor: mcp_agent_tools.list_agent_model_bindings(
                db,
                actor,
                actor_id=actor_id,
                include_disabled=include_disabled,
            ),
        )

    @mcp.tool()
    async def agent_get_model_binding(binding_id: int) -> dict[str, Any]:
        """Read one active or historical actor model binding."""
        return await _tool_call(
            ("planning:read", "admin"),
            lambda db, actor: mcp_agent_tools.get_agent_model_binding(
                db,
                actor,
                binding_id,
            ),
        )

    @mcp.tool()
    async def agent_get_task_routing_assessment(
        task_id: int,
    ) -> dict[str, Any]:
        """Read the current task-version-bound routing assessment."""
        return await _tool_call(
            ROUTING_READ_SCOPE_REQUIREMENT,
            lambda db, actor: mcp_agent_tools.get_task_routing_assessment(
                db,
                actor,
                task_id,
            ),
        )

    @mcp.tool()
    async def agent_list_task_routing_assessments(
        task_id: int,
        limit: int = 100,
    ) -> dict[str, Any]:
        """List bounded append-only routing-assessment history newest first."""
        return await _tool_call(
            ROUTING_READ_SCOPE_REQUIREMENT,
            lambda db, actor: mcp_agent_tools.list_task_routing_assessments(
                db,
                actor,
                task_id,
                limit=limit,
            ),
        )

    @mcp.tool()
    async def agent_create_task_routing_assessment(
        task_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Append an audited assessment for the current task version."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.create_task_routing_assessment(
                db,
                actor,
                task_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_preview_task_routing(
        task_id: int,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Preview candidates without mutating task or assignment state."""
        return await _tool_call(
            ROUTING_READ_SCOPE_REQUIREMENT,
            lambda db, actor: mcp_agent_tools.preview_task_routing(
                db,
                actor,
                task_id,
                payload,
            ),
        )

    @mcp.tool()
    async def agent_create_model_catalog_entry(
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Create a provider-neutral model declaration as an admin actor."""
        return await _tool_call(
            "admin:write",
            lambda db, actor: mcp_agent_tools.create_agent_model_catalog_entry(
                db,
                actor,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_update_model_catalog_entry(
        catalog_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Update one model declaration behind an optimistic revision."""
        return await _tool_call(
            "admin:write",
            lambda db, actor: mcp_agent_tools.update_agent_model_catalog_entry(
                db,
                actor,
                catalog_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_disable_model_catalog_entry(
        catalog_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Soft-disable one model declaration after reconciliation."""
        return await _tool_call(
            "admin:write",
            lambda db, actor: mcp_agent_tools.disable_agent_model_catalog_entry(
                db,
                actor,
                catalog_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_create_model_binding(
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Create one actor model binding as an admin actor."""
        return await _tool_call(
            "admin:write",
            lambda db, actor: mcp_agent_tools.create_agent_model_binding(
                db,
                actor,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_update_model_binding(
        binding_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Update one actor model binding behind an optimistic revision."""
        return await _tool_call(
            "admin:write",
            lambda db, actor: mcp_agent_tools.update_agent_model_binding(
                db,
                actor,
                binding_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_disable_model_binding(
        binding_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Soft-disable one actor model binding after reconciliation."""
        return await _tool_call(
            "admin:write",
            lambda db, actor: mcp_agent_tools.disable_agent_model_binding(
                db,
                actor,
                binding_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_create_assignment(
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Dispatch one task to an exact actor using the durable assignment contract."""
        return await _tool_call(
            "assignments:write",
            lambda db, actor: mcp_agent_tools.create_agent_assignment(
                db,
                actor,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_list_assignments(
        task_id: Optional[int] = None,
        actor_id: Optional[int] = None,
        purpose: Optional[str] = None,
        state: Optional[str] = None,
        limit: int = 200,
    ) -> list[dict[str, Any]]:
        """List durable task assignments for PM restart/reconciliation."""
        return await _tool_call(
            ("assignments:read", "planning:read"),
            lambda db, actor: mcp_agent_tools.list_agent_assignments(
                db,
                actor,
                task_id=task_id,
                actor_id=actor_id,
                purpose=purpose,
                state=state,
                limit=limit,
            ),
        )

    @mcp.tool()
    async def agent_update_assignment(
        assignment_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Reassign, reorder, defer, or cancel a queued durable assignment."""
        return await _tool_call(
            "assignments:write",
            lambda db, actor: mcp_agent_tools.update_agent_assignment(
                db,
                actor,
                assignment_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_get_my_work(
        limit: int = 20,
        cursor: Optional[str] = None,
    ) -> dict[str, Any]:
        """Return the server-authoritative resume, begin, wait, or recovery decision."""
        return await _tool_call(
            ("assignments:read", "tasks:read"),
            lambda db, actor: mcp_agent_tools.get_my_work(
                db,
                actor,
                limit=limit,
                cursor=cursor,
            ),
        )

    @mcp.tool()
    async def agent_list_my_claims() -> list[dict[str, Any]]:
        """List claims currently owned by the authenticated actor."""
        return await _tool_call(
            ("assignments:read", "tasks:read"),
            lambda db, actor: mcp_agent_tools.list_my_claims(db, actor),
        )

    @mcp.tool()
    async def agent_list_my_runs(limit: int = 50) -> list[dict[str, Any]]:
        """List recent runs owned by the authenticated actor."""
        return await _tool_call(
            ("assignments:read", "runs:write"),
            lambda db, actor: mcp_agent_tools.list_my_runs(
                db,
                actor,
                limit=limit,
            ),
        )

    @mcp.tool()
    async def agent_get_complete_task_context(
        task_id: int,
        assignment_id: Optional[int] = None,
    ) -> dict[str, Any]:
        """Return assignment-bound brief, dependency states, readiness, and timeline."""
        return await _tool_call(
            ("assignments:read", "tasks:read", "verification:read"),
            lambda db, actor: mcp_agent_tools.get_complete_task_context(
                db,
                actor,
                task_id,
                assignment_id=assignment_id,
            ),
        )

    @mcp.tool()
    async def agent_begin_my_work(
        payload: dict[str, Any],
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Atomically accept, fence, claim, run, and activate selected work."""
        return await _tool_call(
            "work:execute",
            lambda db, actor: mcp_agent_tools.begin_my_work(
                db,
                actor,
                payload,
                idempotency_key=idempotency_key,
            ),
        )

    @mcp.tool()
    async def agent_renew_my_work(
        payload: dict[str, Any],
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Atomically renew the current assignment fence and run heartbeat."""
        return await _tool_call(
            "work:execute",
            lambda db, actor: mcp_agent_tools.renew_my_work(
                db,
                actor,
                payload,
                idempotency_key=idempotency_key,
            ),
        )

    @mcp.tool()
    async def agent_report_discovery(
        payload: dict[str, Any],
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Report claim-bound out-of-scope work to PM-controlled Triage."""
        return await _tool_call(
            "triage:write",
            lambda db, actor: mcp_agent_tools.report_discovery(
                db,
                actor,
                payload,
                idempotency_key=idempotency_key,
            ),
        )

    @mcp.tool()
    async def agent_submit_my_work(
        payload: dict[str, Any],
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Atomically submit evidence, resolve, fulfill, and release selected work."""
        return await _tool_call(
            "work:execute",
            lambda db, actor: mcp_agent_tools.submit_my_work(
                db,
                actor,
                payload,
                idempotency_key=idempotency_key,
            ),
        )

    @mcp.tool()
    async def agent_fail_my_work(
        payload: dict[str, Any],
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Atomically fail or cancel work and leave a typed recovery signal."""
        return await _tool_call(
            "work:execute",
            lambda db, actor: mcp_agent_tools.fail_my_work(
                db,
                actor,
                payload,
                idempotency_key=idempotency_key,
            ),
        )

    @mcp.tool()
    async def agent_get_my_reviews(
        limit: int = 50,
        cursor: Optional[str] = None,
    ) -> dict[str, Any]:
        """Return this actor's separate verification assignment queue."""
        return await _tool_call(
            ("verification:read", "verification:write"),
            lambda db, actor: mcp_agent_tools.get_my_reviews(
                db,
                actor,
                limit=limit,
                cursor=cursor,
            ),
        )

    @mcp.tool()
    async def agent_submit_review_verdict(
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Record an independent pass/reject verdict and optional rework handoff."""
        return await _tool_call(
            "verification:write",
            lambda db, actor: mcp_agent_tools.submit_review_verdict(
                db,
                actor,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_list_recovery_tasks(
        limit: int = 50,
        cursor: Optional[str] = None,
    ) -> dict[str, Any]:
        """List active tasks with no valid live execution owner."""
        return await _tool_call(
            "recovery:read",
            lambda db, actor: mcp_agent_tools.list_agent_recovery_tasks(
                db,
                actor,
                limit=limit,
                cursor=cursor,
            ),
        )

    @mcp.tool()
    async def agent_requeue_recovery(
        task_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Reconcile stale ownership and dispatch one ordered recovery assignment."""
        return await _tool_call(
            "recovery:write",
            lambda db, actor: mcp_agent_tools.requeue_agent_recovery(
                db,
                actor,
                task_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_get_pipeline() -> dict[str, list[dict[str, Any]]]:
        """Return the complete PM supervision pipeline."""
        return await _tool_call(
            "planning:read",
            lambda db, actor: mcp_agent_tools.get_agent_pipeline(db, actor),
        )

    @mcp.tool()
    async def agent_get_run_detail(run_id: int) -> dict[str, Any] | None:
        """Return one agent run with its chronological events."""
        return await _tool_call(
            "planning:read",
            lambda db, actor: mcp_agent_tools.get_agent_run_detail(
                db,
                actor,
                run_id,
            ),
        )

    @mcp.tool()
    async def agent_list_ready_tasks(
        iteration_id: Optional[int] = None,
        tags: Optional[list[str]] = None,
        priority_min: Optional[int] = None,
        priority_max: Optional[int] = None,
        assignee_id: Optional[int] = None,
        capabilities: Optional[list[str]] = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """List claimable agent-ready tasks."""
        return await _tool_call(
            "tasks:read",
            lambda db, actor: mcp_agent_tools.list_ready_tasks(
                db,
                actor,
                iteration_id=iteration_id,
                tags=tags,
                priority_min=priority_min,
                priority_max=priority_max,
                assignee_id=assignee_id,
                capabilities=capabilities,
                limit=limit,
            ),
        )

    @mcp.tool()
    async def agent_get_task_context(task_id: int) -> dict[str, Any] | None:
        """Get task details plus merged timeline context."""
        return await _tool_call(
            "tasks:read",
            lambda db, actor: mcp_agent_tools.get_task_context(db, actor, task_id),
        )

    @mcp.tool()
    async def agent_claim_task(
        task_id: int,
        lease_seconds: int = 3600,
        idempotency_key: Optional[str] = None,
    ) -> dict[str, Any] | None:
        """Claim a task lease for this agent."""
        return await _tool_call(
            "tasks:write",
            lambda db, actor: mcp_agent_tools.claim_task(
                db,
                actor,
                task_id,
                lease_seconds=lease_seconds,
                idempotency_key=idempotency_key,
            ),
        )

    @mcp.tool()
    async def agent_renew_claim(
        task_id: int,
        lease_seconds: int = 3600,
        idempotency_key: Optional[str] = None,
    ) -> dict[str, Any] | None:
        """Renew this agent's task lease."""
        return await _tool_call(
            "tasks:write",
            lambda db, actor: mcp_agent_tools.renew_task(
                db,
                actor,
                task_id,
                lease_seconds=lease_seconds,
                idempotency_key=idempotency_key,
            ),
        )

    @mcp.tool()
    async def agent_release_task(
        task_id: int,
        idempotency_key: Optional[str] = None,
    ) -> dict[str, Any] | None:
        """Release this agent's task lease."""
        return await _tool_call(
            "tasks:write",
            lambda db, actor: mcp_agent_tools.release_task(
                db,
                actor,
                task_id,
                idempotency_key=idempotency_key,
            ),
        )

    @mcp.tool()
    async def agent_create_task(
        iteration_id: int,
        payload: dict[str, Any],
        idempotency_key: Optional[str] = None,
    ) -> dict[str, Any]:
        """Compatibility task create; PM automation uses agent_create_planning_task."""
        return await _tool_call(
            ("planning:write", "tasks:write"),
            lambda db, actor: mcp_agent_tools.create_task(
                db,
                actor,
                iteration_id,
                payload,
                idempotency_key=idempotency_key,
            ),
        )

    @mcp.tool()
    async def agent_patch_task(
        task_id: int,
        payload: dict[str, Any],
        idempotency_key: Optional[str] = None,
    ) -> dict[str, Any] | None:
        """Compatibility patch; PM automation uses agent_patch_planning_task."""
        return await _tool_call(
            ("planning:write", "tasks:write"),
            lambda db, actor: mcp_agent_tools.update_task(
                db,
                actor,
                task_id,
                payload,
                idempotency_key=idempotency_key,
            ),
        )

    @mcp.tool()
    async def agent_create_planning_task(
        iteration_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Create a decomposed task through an exact audited PM command."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.create_planning_task(
                db,
                actor,
                iteration_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_patch_planning_task(
        task_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Patch decomposition fields through an exact audited PM command."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.patch_planning_task(
                db,
                actor,
                task_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_append_task_event(
        task_id: int,
        payload: dict[str, Any],
        idempotency_key: Optional[str] = None,
    ) -> dict[str, Any] | None:
        """Append an agent-authored task event."""
        return await _tool_call(
            "events:write",
            lambda db, actor: mcp_agent_tools.append_task_event(
                db,
                actor,
                task_id,
                payload,
                idempotency_key=idempotency_key,
            ),
        )

    @mcp.tool()
    async def agent_start_run(
        payload: dict[str, Any],
        idempotency_key: Optional[str] = None,
    ) -> dict[str, Any]:
        """Start an agent run trace."""
        return await _tool_call(
            "runs:write",
            lambda db, actor: mcp_agent_tools.start_agent_run(
                db,
                actor,
                payload,
                idempotency_key=idempotency_key,
            ),
        )

    @mcp.tool()
    async def agent_append_run_event(run_id: int, payload: dict[str, Any]) -> dict[str, Any] | None:
        """Append an event to an agent run."""
        return await _tool_call(
            "runs:write",
            lambda db, actor: mcp_agent_tools.append_run_event(db, actor, run_id, payload),
        )

    @mcp.tool()
    async def agent_finish_run(run_id: int, payload: dict[str, Any]) -> dict[str, Any] | None:
        """Finish an agent run trace."""
        return await _tool_call(
            "runs:write",
            lambda db, actor: mcp_agent_tools.finish_agent_run(db, actor, run_id, payload),
        )

    @mcp.tool()
    async def agent_create_project(
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Create a project through the audited PM planning command adapter."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.create_planning_project(
                db,
                actor,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_update_project(
        project_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Update a project through the audited PM planning command adapter."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.update_planning_project(
                db,
                actor,
                project_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )


    @mcp.tool()
    async def agent_create_project_milestone(
        project_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Create an audited milestone inside one project."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.create_planning_milestone(
                db,
                actor,
                project_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_update_project_milestone(
        project_id: int,
        milestone_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Update an audited milestone inside one project."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.update_planning_milestone(
                db,
                actor,
                project_id,
                milestone_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_delete_project_milestone(
        project_id: int,
        milestone_id: int,
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Delete an audited milestone inside one project."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.delete_planning_milestone(
                db,
                actor,
                project_id,
                milestone_id,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_create_iteration(
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Create an iteration through the audited PM planning command adapter."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.create_planning_iteration(
                db,
                actor,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_update_iteration(
        iteration_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Update an iteration through the audited PM planning command adapter."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.update_planning_iteration(
                db,
                actor,
                iteration_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_create_team_profile(
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Create a reusable team profile through the audited team adapter."""
        return await _tool_call(
            "team:write",
            lambda db, actor: mcp_agent_tools.create_planning_profile(
                db,
                actor,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_update_team_profile(
        profile_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Update a reusable team profile through the audited team adapter."""
        return await _tool_call(
            "team:write",
            lambda db, actor: mcp_agent_tools.update_planning_profile(
                db,
                actor,
                profile_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_create_team_member(
        iteration_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Add one iteration capacity owner through the audited team adapter."""
        return await _tool_call(
            "team:write",
            lambda db, actor: mcp_agent_tools.create_planning_team_member(
                db,
                actor,
                iteration_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_update_team_member(
        member_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Update one iteration capacity owner through the audited team adapter."""
        return await _tool_call(
            "team:write",
            lambda db, actor: mcp_agent_tools.update_planning_team_member(
                db,
                actor,
                member_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_create_vacation(
        member_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Add one vacation period through the audited team adapter."""
        return await _tool_call(
            "team:write",
            lambda db, actor: mcp_agent_tools.create_planning_vacation(
                db,
                actor,
                member_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_update_vacation(
        vacation_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Update one vacation period through the audited team adapter."""
        return await _tool_call(
            "team:write",
            lambda db, actor: mcp_agent_tools.update_planning_vacation(
                db,
                actor,
                vacation_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_preview_schedule(
        iteration_id: int,
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Preview schedule changes without committing task dates."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.preview_planning_schedule(
                db,
                actor,
                iteration_id,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def agent_apply_schedule(
        iteration_id: int,
        expected_task_versions: dict[int, int],
        expected_input_digest: str,
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Apply previewed schedule changes with task-version fencing."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.apply_planning_schedule(
                db,
                actor,
                iteration_id,
                {
                    "expected_task_versions": expected_task_versions,
                    "expected_input_digest": expected_input_digest,
                },
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def workspace_list_iterations() -> list[dict[str, Any]]:
        """List iterations."""
        return await _tool_call("tasks:read", lambda db, actor: mcp_agent_tools.list_iterations(db))

    @mcp.tool()
    async def workspace_get_iteration(iteration_id: int) -> dict[str, Any] | None:
        """Get one iteration."""
        return await _tool_call("tasks:read", lambda db, actor: mcp_agent_tools.get_iteration(db, iteration_id))

    @mcp.tool()
    async def workspace_get_iteration_summary(iteration_id: int) -> dict[str, Any] | None:
        """Return vacation-aware iteration progress and capacity totals."""
        return await _tool_call(
            ("planning:read", "tasks:read"),
            lambda db, actor: mcp_agent_tools.get_iteration_summary(db, iteration_id),
        )

    @mcp.tool()
    async def workspace_get_iteration_gantt(iteration_id: int) -> dict[str, Any]:
        """Return the current read-only schedule and Gantt evidence."""
        return await _tool_call(
            ("planning:read", "tasks:read"),
            lambda db, actor: mcp_agent_tools.get_iteration_gantt(db, iteration_id),
        )

    @mcp.tool()
    async def workspace_list_team_member_profiles() -> list[dict[str, Any]]:
        """List reusable team profiles with advisory capability skills."""
        return await _tool_call(
            ("team:read", "planning:read"),
            lambda db, actor: mcp_agent_tools.list_team_member_profiles(db),
        )

    @mcp.tool()
    async def workspace_get_team_member_profile(profile_id: int) -> dict[str, Any] | None:
        """Return one reusable team profile with advisory capability skills."""
        return await _tool_call(
            ("team:read", "planning:read"),
            lambda db, actor: mcp_agent_tools.get_team_member_profile(db, profile_id),
        )

    @mcp.tool()
    async def workspace_list_iteration_team(iteration_id: int) -> list[dict[str, Any]]:
        """List iteration capacity owners, profile details, and vacations."""
        return await _tool_call(
            ("team:read", "planning:read"),
            lambda db, actor: mcp_agent_tools.list_iteration_team(db, iteration_id),
        )

    @mcp.tool()
    async def workspace_get_team_member_capacity(member_id: int) -> dict[str, Any] | None:
        """Return vacation-aware capacity for one iteration team member."""
        return await _tool_call(
            ("team:read", "planning:read"),
            lambda db, actor: mcp_agent_tools.get_team_member_capacity(db, member_id),
        )

    @mcp.tool()
    async def workspace_get_team_member_workload(member_id: int) -> dict[str, Any] | None:
        """Return allocated, free, and percentage workload for one team member."""
        return await _tool_call(
            ("team:read", "planning:read"),
            lambda db, actor: mcp_agent_tools.get_team_member_workload(db, member_id),
        )

    @mcp.tool()
    async def workspace_list_team_member_vacations(
        member_id: int,
    ) -> list[dict[str, Any]] | None:
        """Return explicit vacation periods for one iteration team member."""
        return await _tool_call(
            ("team:read", "planning:read"),
            lambda db, actor: mcp_agent_tools.list_team_member_vacations(db, member_id),
        )

    @mcp.tool()
    async def workspace_get_profile_skill_catalog() -> list[dict[str, Any]]:
        """Return code-owned advisory capability definitions."""
        return await _tool_call(
            ("planning:read", "team:read", "tasks:read"),
            lambda db, actor: mcp_agent_tools.get_profile_skill_catalog(db),
        )

    @mcp.tool()
    async def workspace_get_agent_profile_presets() -> list[dict[str, Any]]:
        """Return reusable, human-reviewable agent profile presets."""
        return await _tool_call(
            ("planning:read", "team:read", "tasks:read"),
            lambda db, actor: mcp_agent_tools.get_agent_profile_presets(db),
        )

    @mcp.tool()
    async def workspace_get_agent_routes() -> list[dict[str, Any]]:
        """Return the explainable, non-authorizing agent route index."""
        return await _tool_call(
            ("planning:read", "team:read", "tasks:read"),
            lambda db, actor: mcp_agent_tools.get_agent_routes(db),
        )

    @mcp.tool()
    async def workspace_apply_agent_profile_preset(
        preset_key: str,
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Apply one built-in preset through an actor-attributed exact receipt."""
        return await _tool_call(
            "team:write",
            lambda db, actor: mcp_agent_tools.apply_agent_profile_preset(
                db,
                actor,
                preset_key,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def workspace_list_projects() -> list[dict[str, Any]]:
        """List projects."""
        return await _tool_call("tasks:read", lambda db, actor: mcp_agent_tools.list_projects(db))

    @mcp.tool()
    async def workspace_get_project(project_id: int) -> dict[str, Any] | None:
        """Get one project."""
        return await _tool_call("tasks:read", lambda db, actor: mcp_agent_tools.get_project(db, project_id))

    @mcp.tool()
    async def workspace_get_project_summary(project_id: int) -> dict[str, Any] | None:
        """Get project summary."""
        return await _tool_call("tasks:read", lambda db, actor: mcp_agent_tools.get_project_summary(db, project_id))

    @mcp.tool()
    async def workspace_list_project_milestones(
        project_id: int,
    ) -> list[dict[str, Any]] | None:
        """List project milestones in roadmap order."""
        return await _tool_call(
            ("planning:read", "tasks:read"),
            lambda db, actor: mcp_agent_tools.list_project_milestones(
                db, project_id
            ),
        )

    @mcp.tool()
    async def workspace_get_project_milestone(
        project_id: int,
        milestone_id: int,
    ) -> dict[str, Any] | None:
        """Get one milestone inside its project scope."""
        return await _tool_call(
            ("planning:read", "tasks:read"),
            lambda db, actor: mcp_agent_tools.get_project_milestone(
                db, project_id, milestone_id
            ),
        )

    @mcp.tool()
    async def workspace_list_project_updates(
        project_id: int,
    ) -> list[dict[str, Any]] | None:
        """List append-only project health and status updates."""
        return await _tool_call(
            ("planning:read", "tasks:read"),
            lambda db, actor: mcp_agent_tools.list_project_updates(db, project_id),
        )

    @mcp.tool()
    async def agent_create_project_update(
        project_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Append an evidence-backed project update with agent attribution."""
        return await _tool_call(
            "reports:write",
            lambda db, actor: mcp_agent_tools.create_agent_project_update(
                db,
                actor,
                project_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def workspace_list_project_tasks(project_id: int) -> list[dict[str, Any]] | None:
        """List project-linked tasks."""
        return await _tool_call("tasks:read", lambda db, actor: mcp_agent_tools.list_project_tasks(db, project_id))

    @mcp.tool()
    async def workspace_list_triage_items(
        active: Optional[bool] = True,
        statuses: Optional[list[str]] = None,
        q: Optional[str] = None,
        source: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """List triage items."""
        return await _tool_call(
            "tasks:read",
            lambda db, actor: mcp_agent_tools.list_triage_items(
                db,
                active=active,
                statuses=statuses,
                q=q,
                source=source,
                limit=limit,
                offset=offset,
            ),
        )

    @mcp.tool()
    async def workspace_get_triage_item(triage_item_id: int) -> dict[str, Any] | None:
        """Get one triage item."""
        return await _tool_call("tasks:read", lambda db, actor: mcp_agent_tools.get_triage_item(db, triage_item_id))

    @mcp.tool()
    async def workspace_create_triage_item(
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Idempotently create a PM-controlled triage item."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.create_triage_item(
                db,
                actor,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def workspace_classify_triage_item(
        triage_item_id: int,
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any] | None:
        """Idempotently create an advisory triage classification suggestion."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.classify_triage_item(
                db,
                actor,
                triage_item_id,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def workspace_draft_triage_task(
        triage_item_id: int,
        payload: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any] | None:
        """Draft transient task details for triage conversion."""
        return await _tool_call(
            "planning:read",
            lambda db, actor: mcp_agent_tools.draft_triage_task(db, triage_item_id, payload),
        )

    @mcp.tool()
    async def workspace_update_triage_item(
        triage_item_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any] | None:
        """Idempotently update editable triage metadata."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.update_triage_item(
                db,
                actor,
                triage_item_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def workspace_accept_triage_item(
        triage_item_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any] | None:
        """Idempotently accept one triage item."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.accept_triage_item(
                db,
                actor,
                triage_item_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def workspace_decline_triage_item(
        triage_item_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any] | None:
        """Idempotently decline one triage item."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.decline_triage_item(
                db,
                actor,
                triage_item_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def workspace_snooze_triage_item(
        triage_item_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any] | None:
        """Idempotently snooze one triage item."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.snooze_triage_item(
                db,
                actor,
                triage_item_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def workspace_mark_triage_item_duplicate(
        triage_item_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any] | None:
        """Idempotently mark one triage item as duplicate."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.mark_triage_item_duplicate(
                db,
                actor,
                triage_item_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def workspace_convert_triage_to_task(
        triage_item_id: int,
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any] | None:
        """Idempotently convert a locked triage item to one planned task."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.convert_triage_to_task(
                db,
                actor,
                triage_item_id,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def workspace_list_releases(project_id: int) -> list[dict[str, Any]] | None:
        """List releases for a project."""
        return await _tool_call("tasks:read", lambda db, actor: mcp_agent_tools.list_releases_for_project(db, project_id))

    @mcp.tool()
    async def workspace_get_release(release_id: int) -> dict[str, Any] | None:
        """Get one release."""
        return await _tool_call("tasks:read", lambda db, actor: mcp_agent_tools.get_release(db, release_id))

    @mcp.tool()
    async def workspace_list_label_groups(include_inactive: bool = False) -> list[dict[str, Any]]:
        """List governed label groups."""
        return await _tool_call("tasks:read", lambda db, actor: mcp_agent_tools.list_label_groups(db, include_inactive))

    @mcp.tool()
    async def workspace_list_labels(
        group_id: Optional[int] = None,
        group_key: Optional[str] = None,
        include_inactive: bool = False,
    ) -> list[dict[str, Any]]:
        """List governed labels."""
        return await _tool_call(
            "tasks:read",
            lambda db, actor: mcp_agent_tools.list_labels(
                db,
                group_id=group_id,
                group_key=group_key,
                include_inactive=include_inactive,
            ),
        )

    @mcp.tool()
    async def workspace_list_templates(
        template_type: Optional[str] = None,
        include_inactive: bool = False,
    ) -> list[dict[str, Any]]:
        """List work templates."""
        return await _tool_call(
            "tasks:read",
            lambda db, actor: mcp_agent_tools.list_templates(db, template_type, include_inactive),
        )

    @mcp.tool()
    async def workspace_list_saved_views(view_type: Optional[str] = None) -> list[dict[str, Any]]:
        """List shared and system saved views."""
        return await _tool_call("tasks:read", lambda db, actor: mcp_agent_tools.list_saved_views(db, view_type))

    @mcp.tool()
    async def workspace_list_external_links(entity_type: str, entity_id: int) -> list[dict[str, Any]]:
        """List external links for task, project, or release."""
        return await _tool_call(
            "tasks:read",
            lambda db, actor: mcp_agent_tools.list_external_links(db, entity_type, entity_id),
        )

    @mcp.tool()
    async def workspace_create_task_github_link(
        task_id: int,
        url: str,
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Link a GitHub URL to a task with an exact actor-attributed receipt."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.create_task_github_link(
                db,
                actor,
                task_id,
                url,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def workspace_delete_external_link(
        link_id: int,
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Delete an external link with an exact actor-attributed receipt."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.delete_external_link(
                db,
                actor,
                link_id,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def workspace_search_request_sources(
        q: Optional[str] = None,
        source_type: Optional[str] = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Search request sources."""
        return await _tool_call(
            "tasks:read",
            lambda db, actor: mcp_agent_tools.search_request_sources(db, q, source_type, limit),
        )

    @mcp.tool()
    async def workspace_list_request_source_links(target_type: str, target_id: int) -> list[dict[str, Any]]:
        """List request-source links for a target."""
        return await _tool_call(
            "tasks:read",
            lambda db, actor: mcp_agent_tools.list_request_source_links(db, target_type, target_id),
        )

    @mcp.tool()
    async def workspace_create_request_source_link(
        payload: dict[str, Any],
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Create a request-source link with an exact attributed receipt."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.create_request_source_link(
                db,
                actor,
                payload,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def workspace_unlink_request_source(
        link_id: int,
        idempotency_key: str,
        rationale: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        """Unlink a request source with an exact actor-attributed receipt."""
        return await _tool_call(
            "planning:write",
            lambda db, actor: mcp_agent_tools.unlink_request_source(
                db,
                actor,
                link_id,
                idempotency_key=idempotency_key,
                rationale=rationale,
                correlation_id=correlation_id,
            ),
        )

    @mcp.tool()
    async def recommendations_for_task(task_id: int) -> list[dict[str, Any]] | None:
        """Return explainable assignee recommendations for a task."""
        return await _tool_call("tasks:read", lambda db, actor: mcp_agent_tools.recommend_assignees_for_task(db, task_id))

    @mcp.tool()
    async def recommendations_for_triage(
        triage_item_id: int,
        iteration_id: Optional[int] = None,
    ) -> list[dict[str, Any]] | None:
        """Return explainable assignee recommendations for triage intake."""
        return await _tool_call(
            "tasks:read",
            lambda db, actor: mcp_agent_tools.recommend_assignees_for_triage(db, triage_item_id, iteration_id),
        )

    @mcp.tool()
    async def system_get_runtime_config_status() -> dict[str, Any]:
        """Return redacted runtime configuration status. Requires admin scope."""
        return await _tool_call("admin", lambda db, actor: mcp_agent_tools.system_runtime_config_status(db))

    @mcp.resource("workchord://tasks/{task_id}", mime_type="application/json")
    async def task_resource(task_id: str) -> str:
        """Task resource."""
        return await _json_resource(
            "tasks:read",
            lambda db, actor: mcp_agent_tools.get_task(db, actor, int(task_id)),
        )

    @mcp.resource("workchord://tasks/{task_id}/timeline", mime_type="application/json")
    async def task_timeline_resource(task_id: str) -> str:
        """Task timeline resource."""
        return await _json_resource(
            "tasks:read",
            lambda db, actor: mcp_agent_tools.get_task_timeline(db, actor, int(task_id)),
        )

    @mcp.resource("workchord://projects/{project_id}", mime_type="application/json")
    async def project_resource(project_id: str) -> str:
        """Project resource."""
        return await _json_resource(
            "tasks:read",
            lambda db, actor: mcp_agent_tools.get_project(db, int(project_id)),
        )

    @mcp.resource("workchord://triage/{triage_item_id}", mime_type="application/json")
    async def triage_resource(triage_item_id: str) -> str:
        """Triage item resource."""
        return await _json_resource(
            "tasks:read",
            lambda db, actor: mcp_agent_tools.get_triage_item(db, int(triage_item_id)),
        )

    @mcp.resource("workchord://iterations/{iteration_id}", mime_type="application/json")
    async def iteration_resource(iteration_id: str) -> str:
        """Iteration resource."""
        return await _json_resource(
            "tasks:read",
            lambda db, actor: mcp_agent_tools.get_iteration(db, int(iteration_id)),
        )

    @mcp.resource("workchord://releases/{release_id}", mime_type="application/json")
    async def release_resource(release_id: str) -> str:
        """Release resource."""
        return await _json_resource(
            "tasks:read",
            lambda db, actor: mcp_agent_tools.get_release(db, int(release_id)),
        )

    @mcp.resource("workchord://agent/capabilities", mime_type="application/json")
    async def agent_capabilities_resource() -> str:
        """Authenticated actor and server capability resource."""
        return await _json_resource(
            None,
            lambda db, actor: mcp_agent_tools.get_agent_capabilities(db, actor),
        )

    @mcp.resource("workchord://agent/actors", mime_type="application/json")
    async def agent_actor_roster_resource() -> str:
        """Authoritative secret-free exact-actor roster resource."""
        return await _json_resource(
            ("assignments:read", "assignments:write", "planning:read"),
            lambda db, actor: mcp_agent_tools.list_agent_actor_roster(db, actor),
        )

    @mcp.resource("workchord://agent/model-catalog", mime_type="application/json")
    async def agent_model_catalog_resource() -> str:
        """Provider-neutral model capability catalog resource."""
        return await _json_resource(
            ("planning:read", "admin"),
            lambda db, actor: mcp_agent_tools.list_agent_model_catalog(db, actor),
        )

    @mcp.resource(
        "workchord://agent/tasks/{task_id}/routing-assessment",
        mime_type="application/json",
    )
    async def task_routing_assessment_resource(task_id: str) -> str:
        """Current task-version-bound routing assessment resource."""
        return await _json_resource(
            ROUTING_READ_SCOPE_REQUIREMENT,
            lambda db, actor: mcp_agent_tools.get_task_routing_assessment(
                db,
                actor,
                int(task_id),
            ),
        )

    @mcp.resource("workchord://agent/me/work", mime_type="application/json")
    async def agent_work_resource() -> str:
        """Authenticated actor current/next work decision resource."""
        return await _json_resource(
            ("assignments:read", "tasks:read"),
            lambda db, actor: mcp_agent_tools.get_my_work(db, actor),
        )

    @mcp.resource("workchord://agent/me/reviews", mime_type="application/json")
    async def agent_reviews_resource() -> str:
        """Authenticated verifier assignment queue resource."""
        return await _json_resource(
            ("verification:read", "verification:write"),
            lambda db, actor: mcp_agent_tools.get_my_reviews(db, actor),
        )

    @mcp.resource("workchord://agent/tasks/{task_id}/context", mime_type="application/json")
    async def complete_task_context_resource(task_id: str) -> str:
        """Assignment-bound complete task context resource."""
        return await _json_resource(
            ("assignments:read", "tasks:read", "verification:read"),
            lambda db, actor: mcp_agent_tools.get_complete_task_context(
                db,
                actor,
                int(task_id),
            ),
        )

    @mcp.resource("workchord://agent/pipeline", mime_type="application/json")
    async def agent_pipeline_resource() -> str:
        """PM supervision pipeline resource."""
        return await _json_resource(
            "planning:read",
            lambda db, actor: mcp_agent_tools.get_agent_pipeline(db, actor),
        )

    @mcp.resource("workchord://agent/profile-skill-catalog", mime_type="application/json")
    async def profile_skill_catalog_resource() -> str:
        """Advisory capability catalog resource."""
        return await _json_resource(
            ("planning:read", "team:read", "tasks:read"),
            lambda db, actor: mcp_agent_tools.get_profile_skill_catalog(db),
        )

    @mcp.resource("workchord://agent/profile-presets", mime_type="application/json")
    async def agent_profile_presets_resource() -> str:
        """Agent profile preset resource."""
        return await _json_resource(
            ("planning:read", "team:read", "tasks:read"),
            lambda db, actor: mcp_agent_tools.get_agent_profile_presets(db),
        )

    @mcp.resource("workchord://agent/routes", mime_type="application/json")
    async def agent_routes_resource() -> str:
        """Explainable agent route index resource."""
        return await _json_resource(
            ("planning:read", "team:read", "tasks:read"),
            lambda db, actor: mcp_agent_tools.get_agent_routes(db),
        )

    @mcp.resource("workchord://skill-bundles/catalog", mime_type="application/json")
    async def agent_skill_catalog_resource() -> str:
        """Canonical distributable agent skill catalog resource."""
        return await _json_resource(
            _skill_bundle_scope_requirement(),
            lambda db, actor: mcp_agent_tools.get_agent_skill_catalog(),
        )

    @mcp.resource(
        "workchord://skill-bundles/{skill_name}/{skill_version}/manifest",
        mime_type="application/json",
    )
    async def agent_skill_manifest_resource(skill_name: str, skill_version: str) -> str:
        """Exact-version skill manifest resource."""
        return await _json_resource(
            _skill_bundle_scope_requirement(),
            lambda db, actor: mcp_agent_tools.get_agent_skill_manifest(
                skill_name,
                skill_version,
            ),
        )

    @mcp.resource(
        "workchord://skill-bundles/{skill_name}/{skill_version}/SKILL.md",
        mime_type="text/markdown",
    )
    async def agent_skill_entrypoint_resource(
        skill_name: str,
        skill_version: str,
    ) -> str:
        """Hash-verified exact-version SKILL.md resource."""
        return await _tool_call(
            _skill_bundle_scope_requirement(),
            lambda db, actor: mcp_agent_tools.get_agent_skill_entrypoint(
                skill_name,
                skill_version,
            ),
        )

    @mcp.resource(
        "workchord://skill-bundles/{skill_name}/{skill_version}/references/{reference_name}",
        mime_type="text/markdown",
    )
    async def agent_skill_reference_resource(
        skill_name: str,
        skill_version: str,
        reference_name: str,
    ) -> str:
        """Hash-verified direct Markdown reference from an exact skill version."""
        return await _tool_call(
            _skill_bundle_scope_requirement(),
            lambda db, actor: mcp_agent_tools.get_agent_skill_reference(
                skill_name,
                skill_version,
                reference_name,
            ),
        )

    @mcp.prompt()
    async def workchord_pm_role() -> str:
        """Point a PM client to the exact canonical controller role."""
        return await _skill_bundle_prompt(
            "Read workchord://agent/capabilities, resolve its recommended PM skill version, "
            "then read workchord://skill-bundles/workchord-pm/{version}/SKILL.md. "
            "Follow that controller skill and its referenced files; do not infer authority "
            "from profile capability matches."
        )

    @mcp.prompt()
    async def workchord_worker_role() -> str:
        """Point a worker client to the exact canonical assigned-work role."""
        return await _skill_bundle_prompt(
            "Read workchord://agent/capabilities, resolve its recommended worker skill version, "
            "then read workchord://skill-bundles/workchord-worker/{version}/SKILL.md. "
            "Follow that skill, call workchord://agent/me/work, and execute only the exact "
            "server-selected assignment."
        )

    @mcp.prompt()
    def task_implementation_brief(task_id: str) -> str:
        """Prompt for implementing one WorkChord task."""
        return (
            f"Use workchord://tasks/{task_id} and workchord://tasks/{task_id}/timeline. "
            "Summarize scope, blockers, acceptance criteria, and the exact next implementation steps."
        )

    @mcp.prompt()
    def triage_to_task_draft(triage_item_id: str) -> str:
        """Prompt for drafting a task from triage intake."""
        return (
            f"Use workchord://triage/{triage_item_id}. Draft a concise task title, detailed description, "
            "acceptance criteria, risks, and suggested labels without mutating the item."
        )

    @mcp.prompt()
    def task_progress_event(task_id: str) -> str:
        """Prompt for appending a structured task progress event."""
        return (
            f"Prepare an agent_append_task_event payload for task {task_id} with event_type, "
            "payload.summary, payload.next_steps, trace_id, span_id, and correlation_id."
        )

    @mcp.prompt()
    def blocker_explanation(task_id: str) -> str:
        """Prompt for explaining why a task is blocked."""
        return (
            f"Use workchord://tasks/{task_id} and its timeline to explain blockers, dependency state, "
            "claim state, and the lowest-risk unblocking action."
        )

    @mcp.prompt()
    def status_update_draft(project_id: str) -> str:
        """Prompt for drafting a project status update."""
        return (
            f"Use workchord://projects/{project_id} and related task/release tools. Draft a stakeholder update "
            "with progress, risks, decisions, and next steps."
        )

    return mcp


mcp = create_mcp_server()


def create_mcp_http_app() -> ASGIApp:
    """Return the authenticated Streamable HTTP MCP ASGI app."""
    return MCPHostValidationMiddleware(
        MCPAgentKeyMiddleware(mcp.streamable_http_app())
    )


def mount_mcp_http(app: Any, path: str) -> None:
    """Mount authenticated Streamable HTTP MCP at both `/path` and `/path/`."""
    normalized_path = path.rstrip("/")
    mcp_http_app = create_mcp_http_app()
    app.router.routes.append(
        Route(
            normalized_path,
            MCPExactPathAlias(mcp_http_app, normalized_path),
            include_in_schema=False,
        )
    )
    app.mount(normalized_path, mcp_http_app, name="mcp")


async def _run_standalone_transport(transport: str) -> None:
    """Run and dispose a standalone transport on one event loop."""

    try:
        if transport == "stdio":
            await mcp.run_stdio_async()
        else:
            await mcp.run_streamable_http_async()
    finally:
        await close_database()


def main(argv: Optional[list[str]] = None) -> None:
    """Run the standalone MCP server."""
    parser = argparse.ArgumentParser(description="Run WorkChord MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="MCP transport to run",
    )
    args = parser.parse_args(argv)

    if args.transport == "stdio" and not os.getenv(MCP_AGENT_API_KEY_ENV):
        print(f"{MCP_AGENT_API_KEY_ENV} is required for stdio MCP", file=sys.stderr)
        raise SystemExit(2)

    if args.transport == "stdio":
        # Stdio MCP reserves stdout for protocol frames; startup output must go to stderr.
        with redirect_stdout(sys.stderr):
            asyncio.run(init_db())
    else:
        asyncio.run(init_db())
    asyncio.run(_run_standalone_transport(args.transport))


if __name__ == "__main__":
    main()
