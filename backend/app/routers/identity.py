"""Human sign-in, owner bootstrap, membership and session management."""

from datetime import datetime, timedelta
from typing import Annotated, Literal
import secrets

from fastapi import APIRouter, Depends, Request, Response, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select, update

from app.authority import Authority, AuthorityError, internal_authority, require_operator
from app.commands import commit_or_flush
from app.config import get_settings
from app.database import get_db
from app.http_authority import resolve_http_identity
from app.models.identity import Principal, WorkspaceMembership, WorkspaceAuthorityState, ProjectMembership, PrincipalProfileLink, CommandAudit
from app.models.user_session import UserSession
from app.security import require_admin_api_key
from app.services.identity_service import IdentityService, require_identity_writes
from app.services.session_service import _cookie_options, get_client_ip
from app.utils.time import utc_now

router = APIRouter(prefix="/auth")
Database = Annotated[object, Depends(get_db, scope="function")]


class BootstrapOwner(BaseModel):
    principal_id: int = Field(ge=1)


class NativeConnectionStart(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code_challenge: str = Field(pattern=r"^[A-Za-z0-9_-]{43}$")


class NativeConnectionExchange(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str = Field(pattern=r"^[A-Za-z0-9_-]{43}$")
    code_verifier: str = Field(pattern=r"^[A-Za-z0-9._~-]{43,128}$")


class NativeConnectionApproval(BaseModel):
    model_config = ConfigDict(extra="forbid")
    verification_code: str = Field(pattern=r"^[A-Z2-9]{4}-[A-Z2-9]{4}$")


class NativeConnectionResponse(BaseModel):
    request_id: str
    verification_code: str
    verification_path: str
    expires_at: datetime


class NativeConnectionDetails(BaseModel):
    verification_code: str
    expires_at: datetime
    approved: bool


class NativeApprovalResponse(BaseModel):
    approved: Literal[True]


class NativePendingResponse(BaseModel):
    status: Literal["pending"]


class NativeTokenResponse(BaseModel):
    access_token: str
    token_type: Literal["Bearer"]
    expires_at: datetime


@router.post("/native-connections/start", status_code=201, response_model=NativeConnectionResponse)
async def start_native_connection(data: NativeConnectionStart, request: Request, response: Response, db: Database):
    from app.services.native_session_service import NativeSessionService
    response.headers["Cache-Control"] = "no-store"
    return await NativeSessionService(db).start(data.code_challenge, await get_client_ip(request))


@router.post("/native-connections/exchange", response_model=NativePendingResponse | NativeTokenResponse)
async def exchange_native_connection(data: NativeConnectionExchange, request: Request, response: Response, db: Database):
    from app.services.native_session_service import NativeSessionService
    response.headers["Cache-Control"] = "no-store"
    return await NativeSessionService(db).exchange(data.request_id, data.code_verifier,
        await get_client_ip(request), request.headers.get("User-Agent"))


@router.get("/native-connections/{request_id}", response_model=NativeConnectionDetails)
async def describe_native_connection(request_id: str, response: Response, db: Database):
    from app.services.native_session_service import NativeSessionService
    response.headers["Cache-Control"] = "no-store"
    return await NativeSessionService(db).describe(request_id)


@router.post("/native-connections/{request_id}/approve", response_model=NativeApprovalResponse)
async def approve_native_connection(request_id: str, data: NativeConnectionApproval, response: Response, db: Database):
    from app.services.native_session_service import NativeSessionService
    response.headers["Cache-Control"] = "no-store"
    return await NativeSessionService(db).approve(request_id, data.verification_code)


class MembershipChange(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: Literal["owner", "operator", "member", "viewer", "editor", "executor", "reviewer", "manager"] | None
    reason: str = Field(min_length=8, max_length=2000)


class ProfileLinkRequest(BaseModel):
    profile_id: int = Field(ge=1)
    reason: str = Field(min_length=8, max_length=2000)


class GuestTransferRequest(BaseModel):
    guest_token: str | None = Field(default=None, max_length=128)
    guest_session_id: int | None = Field(default=None, ge=1)
    principal_id: int | None = Field(default=None, ge=1)
    reason: str | None = Field(default=None, max_length=2000)


@router.get("/me")
async def me(request: Request, response: Response, db: Database):
    response.headers["Cache-Control"] = "no-store"
    authentication_error = None
    try:
        authority = await resolve_http_identity(request, db)
    except AuthorityError as exc:
        if exc.code == "conflicting_credentials":
            raise
        authority, authentication_error = None, exc.code
    settings = get_settings()
    result = {"mode": settings.workchord_auth_mode, "authenticated": authority is not None and authority.principal_id is not None,
              "configured": bool(settings.oidc_issuer_url and settings.oidc_client_id and settings.oidc_redirect_uri),
              "principal": None, "profile": None, "csrf_token": None, "workspace_role": None, "projects": {}, "authentication_error": authentication_error}
    if authority is not None and authority.principal_id is not None:
        principal = await db.get(Principal, authority.principal_id)
        result.update(principal={"id": principal.id, "kind": principal.kind, "display_name": principal.display_name},
                      workspace_role=authority.workspace_role, projects=authority.projects)
        if authority.profile_id is not None:
            from app.models.team_member import TeamMemberProfile
            profile = await db.get(TeamMemberProfile, authority.profile_id)
            result["profile"] = {"id": profile.id, "display_name": profile.display_name} if profile else None
        if authority.session_id:
            session = await db.get(UserSession, authority.session_id)
            result["csrf_token"] = session.csrf_token
    return result


@router.get("/login")
async def login(request: Request, db: Database, return_to: str = "/"):
    url, browser = await IdentityService(db).begin_login(return_to)
    response = RedirectResponse(url, status_code=303, headers={"Cache-Control": "no-store"})
    options = _cookie_options()
    response.set_cookie("workchord_login", browser, max_age=600, httponly=True, secure=options["secure"], samesite="lax", path=options["path"])
    guest = request.cookies.get(get_settings().session_cookie_name)
    from app.services.session_service import _get_session_by_token
    guest_session = await _get_session_by_token(db, guest)
    if guest_session is not None and guest_session.principal_id is None:
        response.set_cookie("workchord_guest_transfer", guest, max_age=600, httponly=True, secure=options["secure"], samesite="lax", path=options["path"])
    return response


@router.get("/callback")
async def callback(request: Request, db: Database, code: str, state: str):
    session, raw, target = await IdentityService(db).finish_login(code, state, request.cookies.get("workchord_login"),
        ip_address=await get_client_ip(request), user_agent=request.headers.get("User-Agent"))
    response = RedirectResponse(target, status_code=303, headers={"Cache-Control": "no-store"})
    options = _cookie_options()
    options["max_age"] = get_settings().auth_session_max_age_seconds
    response.set_cookie(value=raw, **options)
    response.delete_cookie("workchord_login", path=options["path"], secure=options["secure"], httponly=True, samesite="lax")
    return response


@router.post("/bootstrap")
async def bootstrap(data: BootstrapOwner, db: Database, _operator: Annotated[None, Depends(require_admin_api_key)]):
    require_identity_writes()
    with internal_authority(db):
        principal = await db.get(Principal, data.principal_id)
        if principal is None or principal.kind != "human" or not principal.enabled:
            raise AuthorityError("principal_not_found", "Sign in once to establish the owner's verified principal.", 404)
        state = await db.get(WorkspaceAuthorityState, 1)
        if state is None:
            raise AuthorityError("identity_migration_required", "Apply the identity migration first.", 503)
        if state.bootstrap_principal_id == principal.id:
            return {"bootstrapped": False, "already_bootstrapped": True}
        changed = await db.execute(update(WorkspaceAuthorityState).where(WorkspaceAuthorityState.id == 1, WorkspaceAuthorityState.bootstrap_principal_id.is_(None))
                                  .values(bootstrap_principal_id=principal.id))
        if changed.rowcount != 1:
            raise AuthorityError("owner_already_bootstrapped", "An owner has already been bootstrapped. Use explicit membership administration.", 409)
        db.add(WorkspaceMembership(principal_id=principal.id, role="owner"))
        db.add(CommandAudit(principal_id=state.operator_principal_id, action="workspace_owner_bootstrapped", source="operator",
                            correlation_id=secrets.token_hex(16), reason="One-time owner bootstrap using the configured operator credential",
                            details={"principal_id": principal.id}))
        return {"bootstrapped": True, "principal_id": principal.id}


@router.get("/principals")
async def list_principals(db: Database, limit: int = Query(100, ge=1, le=500)):
    require_operator(db)
    rows = (await db.scalars(select(Principal).order_by(Principal.id).limit(limit))).all()
    return [{"id": p.id, "kind": p.kind, "display_name": p.display_name, "enabled": p.enabled, "agent_actor_id": p.agent_actor_id} for p in rows]


@router.put("/workspace-members/{principal_id}")
async def workspace_member(principal_id: int, data: MembershipChange, db: Database):
    require_operator(db)
    require_identity_writes()
    authority = db.info["authority"]
    if data.role not in {None, "owner", "operator", "member"}:
        raise AuthorityError("invalid_workspace_role", "Choose a workspace role.", 422)
    if data.role == "owner" and authority.workspace_role != "owner" and authority.kind != "system":
        raise AuthorityError()
    with internal_authority(db):
        if await db.get(Principal, principal_id) is None:
            raise AuthorityError("principal_not_found", "Principal not found.", 404)
        existing = await db.get(WorkspaceMembership, principal_id)
        if data.role is None:
            if existing:
                await db.delete(existing)
        elif existing:
            existing.role = data.role
        else:
            db.add(WorkspaceMembership(principal_id=principal_id, role=data.role))
        db.add(CommandAudit(principal_id=authority.principal_id, action="workspace_membership_changed", source=authority.source,
            correlation_id=authority.correlation_id, reason=data.reason, details={"principal_id": principal_id, "role": data.role}))
        await db.flush()
    return {"principal_id": principal_id, "role": data.role}


@router.put("/project-members/{project_id}/{principal_id}")
async def project_member(project_id: int, principal_id: int, data: MembershipChange, db: Database):
    authority = db.info["authority"]
    if not authority.allows(project_id, "manage"):
        raise AuthorityError()
    require_identity_writes()
    if data.role not in {None, "viewer", "editor", "executor", "reviewer", "manager"}:
        raise AuthorityError("invalid_project_role", "Choose a project role.", 422)
    from app.models.project import Project
    with internal_authority(db):
        if await db.get(Principal, principal_id) is None or await db.get(Project, project_id) is None:
            raise AuthorityError("resource_not_found", "Principal or project not found.", 404)
        existing = await db.get(ProjectMembership, (principal_id, project_id))
        if data.role is None:
            if existing:
                await db.delete(existing)
        elif existing:
            existing.role = data.role
        else:
            db.add(ProjectMembership(principal_id=principal_id, project_id=project_id, role=data.role))
        db.add(CommandAudit(principal_id=authority.principal_id, project_id=project_id, action="project_membership_changed", source=authority.source,
            correlation_id=authority.correlation_id, reason=data.reason, details={"principal_id": principal_id, "role": data.role}))
        await db.flush()
    return {"principal_id": principal_id, "project_id": project_id, "role": data.role}


@router.put("/principals/{principal_id}/profile")
async def link_profile(principal_id: int, data: ProfileLinkRequest, db: Database):
    require_operator(db)
    require_identity_writes()
    from app.models.team_member import TeamMemberProfile
    with internal_authority(db):
        principal = await db.get(Principal, principal_id)
        profile = await db.get(TeamMemberProfile, data.profile_id)
        if principal is None or profile is None:
            raise AuthorityError("resource_not_found", "Principal or profile not found.", 404)
        other = await db.scalar(select(PrincipalProfileLink).where(PrincipalProfileLink.profile_id == profile.id))
        if other is not None and other.principal_id != principal_id:
            raise AuthorityError("profile_already_linked", "This profile already belongs to another principal.", 409)
        link = await db.get(PrincipalProfileLink, principal_id)
        if link:
            link.profile_id, link.linked_by_principal_id = profile.id, db.info["authority"].principal_id
        else:
            db.add(PrincipalProfileLink(principal_id=principal_id, profile_id=profile.id, linked_by_principal_id=db.info["authority"].principal_id))
        authority = db.info["authority"]
        db.add(CommandAudit(principal_id=authority.principal_id, action="principal_profile_linked", source=authority.source,
            correlation_id=authority.correlation_id, reason=data.reason, details={"principal_id": principal_id, "profile_id": profile.id}))
        await db.flush()
    return {"principal_id": principal_id, "profile_id": data.profile_id}


@router.post("/transfer-guest")
async def transfer_guest(data: GuestTransferRequest, request: Request, response: Response, db: Database):
    authority = db.info["authority"]
    result = await IdentityService(db).transfer_guest(data.guest_token or request.cookies.get("workchord_guest_transfer"),
        data.principal_id or authority.principal_id, operator_reason=data.reason, guest_id=data.guest_session_id)
    response.delete_cookie("workchord_guest_transfer", path=_cookie_options()["path"])
    return result


@router.post("/native-token", response_model=NativeTokenResponse)
async def native_token(request: Request, response: Response, db: Database):
    authority = db.info["authority"]
    if authority.kind != "human":
        raise AuthorityError()
    session, raw = await IdentityService(db).issue_session(authority.principal_id, await get_client_ip(request), request.headers.get("User-Agent"))
    response.headers["Cache-Control"] = "no-store"
    return {"access_token": raw, "token_type": "Bearer", "expires_at": session.expires_at}


@router.get("/sessions")
async def sessions(db: Database):
    authority = db.info["authority"]
    if authority.principal_id is None:
        raise AuthorityError("authentication_required", "Sign in to manage sessions.", 401)
    rows = (await db.scalars(select(UserSession).where(UserSession.principal_id == authority.principal_id).order_by(UserSession.created_at.desc()).limit(100))).all()
    return [{"public_id": row.public_id, "created_at": row.created_at, "expires_at": row.expires_at,
             "revoked_at": row.revoked_at, "user_agent": row.user_agent, "current": row.id == authority.session_id} for row in rows]


@router.delete("/sessions/{public_id}")
async def revoke_owned_session(public_id: str, db: Database):
    require_identity_writes()
    authority = db.info["authority"]
    with internal_authority(db):
        session = await db.scalar(select(UserSession).where(UserSession.public_id == public_id, UserSession.principal_id == authority.principal_id))
        if session is None or authority.principal_id is None:
            raise AuthorityError("session_not_found", "Session not found.", 404)
        session.revoked_at, session.csrf_token = utc_now(), None
    return {"revoked": True}


@router.post("/logout")
async def logout(response: Response, db: Database):
    require_identity_writes()
    authority = db.info["authority"]
    if authority.session_id:
        with internal_authority(db):
            session = await db.get(UserSession, authority.session_id)
            session.revoked_at, session.csrf_token = utc_now(), None
    options = _cookie_options()
    response.delete_cookie(options["key"], path=options["path"], secure=options["secure"], httponly=True, samesite="lax")
    response.headers["Cache-Control"] = "no-store"
    return {"signed_out": True}


@router.post("/sessions/cleanup")
async def cleanup(db: Database, limit: int = Query(100, ge=1, le=500)):
    return await IdentityService(db).cleanup_sessions(limit=limit)


class PrincipalRecoveryRequest(BaseModel):
    enabled: bool
    reason: str = Field(min_length=8, max_length=2000)


@router.put("/principals/{principal_id}")
async def recover_principal(principal_id: int, data: PrincipalRecoveryRequest, db: Database):
    require_operator(db)
    require_identity_writes()
    authority = db.info["authority"]
    with internal_authority(db):
        principal = await db.get(Principal, principal_id)
        if principal is None:
            raise AuthorityError("principal_not_found", "Principal not found.", 404)
        principal.enabled = data.enabled
        if not data.enabled:
            await db.execute(update(UserSession).where(UserSession.principal_id == principal_id, UserSession.revoked_at.is_(None))
                             .values(revoked_at=utc_now(), csrf_token=None))
        db.add(CommandAudit(principal_id=authority.principal_id, action="principal_access_changed", source=authority.source,
            correlation_id=authority.correlation_id, reason=data.reason, details={"principal_id": principal_id, "enabled": data.enabled}))
        await db.flush()
    return {"principal_id": principal_id, "enabled": data.enabled, "old_sessions_remain_revoked": True}
