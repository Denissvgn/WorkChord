"""Fail-closed HTTP identity resolution and explicit public capability boundaries."""

from dataclasses import replace
import secrets
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy import select

from app.authority import Authority, AuthorityError, internal_authority
from app.database import get_db
from app.config import get_settings
from app.models.identity import Principal, WorkspaceAuthorityState
from app.services.identity_service import IdentityService
from app.services.session_service import _get_session_by_token
from app.security import admin_api_key_is_valid


PUBLIC_PATHS = {"/health", "/health/live", "/health/ready", "/.well-known/workchord-build.json", "/openapi.json", "/docs", "/redoc", "/docs/oauth2-redirect"}
AUTH_PUBLIC_PATHS = {"/auth/me", "/auth/login", "/auth/callback", "/auth/bootstrap"}
OPERATOR_PREFIXES = ("/system-settings", "/settings", "/email-settings", "/scheduling-rules", "/outbound-webhooks", "/github/status-automation-rules")
KNOWN_PREFIXES = ("/tasks", "/iterations", "/projects", "/initiatives", "/milestones", "/releases", "/roadmap", "/team", "/calendars",
                  "/employees", "/vacations", "/request-source-links",
                  "/triage", "/labels", "/label-groups", "/templates", "/saved-views", "/plan-shares", "/request-sources",
                  "/external-links", "/llm", "/agent", "/session", "/auth", "/github", "/export", *OPERATOR_PREFIXES)


def public_capability(path, method):
    if path in {"/intake/web", "/github/webhooks"} and method == "POST":
        return True
    if path.startswith("/plan-shares/") and path.count("/") == 2 and method == "GET":
        return True
    if path.startswith("/agent/skill-bundles") and method == "GET" and get_settings().agent_skill_bundles_public:
        return True
    return False


async def resolve_http_identity(request, db):
    settings = get_settings()
    contexts = []
    identity = IdentityService(db)
    agent_key = request.headers.get("X-Agent-API-Key")
    admin_key = request.headers.get("X-Admin-API-Key")
    authorization = request.headers.get("Authorization")
    with internal_authority(db):
        if agent_key:
            from app.services.agent_service import AgentService
            actor = await AgentService(db).authenticate(agent_key, touch=False)
            if actor is None:
                bootstrap = settings.agent_bootstrap_api_key and secrets.compare_digest(agent_key, settings.agent_bootstrap_api_key)
                relative = request.url.path.removeprefix(settings.api_prefix)
                allowed = relative.startswith(("/agent/actors", "/agent/team-setup", "/agent/model-catalog", "/agent/model-bindings"))
                if not bootstrap or not allowed:
                    raise AuthorityError("authentication_required", "The credential is invalid or unavailable for this operation.", 401)
                state = await db.get(WorkspaceAuthorityState, 1)
                principal = await db.get(Principal, state.operator_principal_id) if state and state.operator_principal_id else None
                if principal is None or not principal.enabled:
                    raise AuthorityError("identity_migration_required", "Apply the identity migration before bootstrap provisioning.", 503)
                contexts.append(Authority(principal.id, "system", workspace_role="operator", source="agent_bootstrap"))
            else:
                contexts.append(await identity.actor_context(actor))
        if admin_key:
            if not admin_api_key_is_valid(admin_key):
                raise AuthorityError("authentication_required", "The operator credential is invalid.", 401)
            state = await db.get(WorkspaceAuthorityState, 1)
            if state is None or state.operator_principal_id is None:
                raise AuthorityError("identity_migration_required", "Apply the identity migration before using operator access.", 503)
            principal = await db.get(Principal, state.operator_principal_id)
            if principal is None or principal.kind != "system" or not principal.enabled:
                raise AuthorityError("authentication_required", "The operator identity is disabled.", 401)
            contexts.append(Authority(state.operator_principal_id, "system", workspace_role="operator"))
        raw_cookie = request.cookies.get(settings.session_cookie_name)
        cookie_session = await _get_session_by_token(db, raw_cookie)
        if raw_cookie and cookie_session is None and settings.workchord_auth_mode == "managed":
            from app.models.user_session import UserSession
            from app.services.identity_service import digest
            stored = await db.scalar(select(UserSession).where(UserSession.session_token_hash == digest(raw_cookie)))
            code = "session_revoked" if stored is not None and stored.revoked_at is not None else "session_expired" if stored is not None else "authentication_required"
            raise AuthorityError(code, "Sign in again to continue.", 401)
        tokens = []
        if cookie_session is not None and cookie_session.principal_id is not None:
            tokens.append(cookie_session)
        if authorization:
            scheme, _, token = authorization.partition(" ")
            if scheme.lower() != "bearer" or not token:
                raise AuthorityError("authentication_required", "Use a supported credential.", 401)
            bearer_session = await _get_session_by_token(db, token)
            if bearer_session is None or bearer_session.principal_id is None:
                raise AuthorityError("authentication_required", "The session credential is invalid or expired.", 401)
            tokens.append(bearer_session)
        for session in tokens:
            principal = await db.get(Principal, session.principal_id)
            if principal is None or not principal.enabled or principal.kind != "human":
                raise AuthorityError("account_disabled", "This account is disabled.", 401)
            contexts.append(await identity.context(principal, session=session))
    identities = {ctx.principal_id for ctx in contexts}
    if len(identities) > 1:
        raise AuthorityError("conflicting_credentials", "Use one account or agent credential per request.", 401)
    authority = contexts[0] if contexts else None
    if cookie_session is not None and cookie_session.principal_id is not None and request.method not in {"GET", "HEAD", "OPTIONS"}:
        supplied = request.headers.get("X-CSRF-Token", "")
        origin = request.headers.get("Origin")
        if origin and origin not in settings.cors_origins or not cookie_session.csrf_token or not secrets.compare_digest(supplied, cookie_session.csrf_token):
            raise AuthorityError("request_integrity_required", "Reload your session before submitting this change.")
    if authority is None and settings.workchord_auth_mode == "trusted_local":
        authority = Authority(None, "local", session_id=cookie_session.id if cookie_session else None, local=True)
    if authority is not None:
        reason = request.headers.get("X-Command-Reason")
        authority = replace(authority, reason=reason[:2000] if reason else None,
            review_override=request.headers.get("X-Review-Override") == "true",
            correlation_id=request.headers.get("X-Correlation-ID", authority.correlation_id)[:128])
    return authority


async def enforce_http_authority(request: Request, db: Annotated[object, Depends(get_db, scope="function")]):
    path = request.url.path
    if path in PUBLIC_PATHS or path.startswith("/.well-known/workchord/agent"):
        return
    prefix = get_settings().api_prefix
    relative = path[len(prefix):] if path.startswith(prefix + "/") else path
    if request.method == "OPTIONS":
        return
    if relative == "/agent/team-setup/onboarding/acknowledge" and request.method == "POST":
        # This credential is intentionally inactive for ordinary agent APIs.
        # The exact handoff handler verifies it before acquiring integration authority.
        if request.headers.get("Authorization") or request.headers.get("X-Admin-API-Key") or request.cookies.get(get_settings().session_cookie_name):
            raise AuthorityError("conflicting_credentials", "Use only the restricted onboarding credential for acknowledgement.", 401)
        return
    if relative in AUTH_PUBLIC_PATHS or public_capability(relative, request.method):
        return
    authority = await resolve_http_identity(request, db)
    if authority is None:
        raise AuthorityError("authentication_required", "Sign in to continue.", 401)
    if relative.startswith("/agent/"):
        authority = replace(authority, source="agent_rest")
    elif authority.kind == "agent":
        read = request.method in {"GET", "HEAD"}
        required = {"tasks:read", "planning:read", "admin"} if read else {"tasks:write", "planning:write", "admin"}
        if relative.startswith(("/team", "/employees", "/vacations")):
            required = {"team:read", "admin"} if read else {"team:write", "admin"}
        if not authority.scopes.intersection(required) and not relative.endswith("/status"):
            raise AuthorityError("agent_scope_required", "The agent credential does not permit this operation.")
    request.state.authority = authority
    db.info["authority"] = authority
    if path in {"/health/ready", "/metrics"}:
        if not authority.operator and not authority.local:
            raise AuthorityError()
        return
    if not relative.startswith(KNOWN_PREFIXES):
        raise AuthorityError("unclassified_route", "This operation has no configured access policy.")
    if request.method not in {"GET", "HEAD"} and relative.startswith("/tasks/"):
        from app.authority import require_project
        from app.models.task import Task
        task_id = request.path_params.get("task_id")
        if task_id is not None:
            task = await db.get(Task, int(task_id))
            if task is None:
                raise AuthorityError("resource_unavailable", "Task not found or inaccessible.", 404)
            action = "edit"
            if relative.endswith("/progress"):
                action = "execute"
            elif relative.endswith("/review"):
                action = "review"
            elif relative.endswith("/commands"):
                payload = await request.json()
                command = payload.get("action") if isinstance(payload, dict) else None
                action = "execute" if command in {"start_manual", "resolve_manual"} else "manage" if command in {"cancel", "reopen"} else "edit"
            if relative.endswith("/status"):
                payload = await request.json()
                action = "review" if isinstance(payload, dict) and payload.get("status") == "closed" else "execute"
                if action == "review" and authority.kind == "agent" and authority.actor_role != "verifier":
                    raise AuthorityError("independent_review_required", "Execution cannot accept its own work.")
            require_project(db, task.project_id, action)
    if relative.startswith("/llm") and request.method not in {"GET", "HEAD"} and not (authority.operator or authority.local or any(role in {"editor", "manager"} for role in authority.projects.values()) or authority.allows(None, "edit")):
        raise AuthorityError()
    if relative.startswith(OPERATOR_PREFIXES) and not authority.operator:
        raise AuthorityError("operator_required", "Workspace operator permission is required.")
    if relative.startswith("/agent") and authority.kind not in {"agent", "system"} and not authority.operator and not authority.local:
        if request.method not in {"GET", "HEAD"}:
            raise AuthorityError()
