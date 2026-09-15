"""Trusted OIDC sign-in and durable principal/session lifecycle."""

import base64
from dataclasses import replace
from datetime import timedelta
import hashlib
import json
import secrets
from urllib.parse import urlencode, urlsplit, unquote

import httpx
import jwt
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from app.authority import Authority, AuthorityError, internal_authority, require_operator
from app.commands import atomic_command, commit_or_flush
from app.config import get_settings
from app.maintenance import MaintenanceModeError
from app.models.identity import (Principal, IdentitySubject, WorkspaceMembership, WorkspaceAuthorityState,
    ProjectMembership, PrincipalProfileLink, OIDCLoginAttempt, OwnershipTransfer, CommandAudit)
from app.models.user_session import UserSession
from app.utils.time import utc_now, as_utc


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def require_identity_writes():
    if get_settings().maintenance_mode != "off":
        raise MaintenanceModeError(operation="identity lifecycle", mode=get_settings().maintenance_mode)


def safe_return_path(value: str) -> str:
    decoded = value
    for _ in range(4):
        next_value = unquote(decoded)
        if next_value == decoded:
            break
        decoded = next_value
    if decoded.startswith("//") or "\\" in decoded or any(ord(c) < 32 for c in decoded):
        return "/"
    if not value.startswith("/") or value.startswith("//") or "\\" in value or any(ord(c) < 32 for c in value):
        return "/"
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or value.startswith("/api/"):
        return "/"
    return value[:512]


def oidc_url(value: str) -> str:
    settings = get_settings()
    parsed = urlsplit(value)
    local_http = (settings.oidc_allow_http_loopback and settings.deployment_environment != "production"
                  and parsed.hostname in {"localhost", "127.0.0.1", "::1", "oidc"})
    if not parsed.hostname or parsed.username or parsed.password or parsed.fragment or parsed.scheme != "https" and not (parsed.scheme == "http" and local_http):
        raise AuthorityError("identity_configuration_required", "Configure a trusted HTTPS OIDC provider and callback.", 503)
    return value


async def provider_json(client: httpx.AsyncClient, method, url, **kwargs):
    try:
        async with client.stream(method, oidc_url(url), **kwargs) as response:
            response.raise_for_status()
            body = bytearray()
            async for chunk in response.aiter_bytes():
                body.extend(chunk)
                if len(body) > 1024 * 1024:
                    raise AuthorityError("identity_provider_error", "The identity provider returned an oversized response.", 502)
        value = json.loads(body)
        if not isinstance(value, dict):
            raise ValueError("Object required")
        return value
    except (httpx.HTTPError, ValueError) as exc:
        raise AuthorityError("identity_provider_unavailable", "Sign-in is temporarily unavailable. Start again when the identity provider is reachable.", 503) from exc


async def provider_configuration(client):
    settings = get_settings()
    if not settings.oidc_client_id or not settings.oidc_issuer_url or not settings.oidc_redirect_uri:
        raise AuthorityError("identity_configuration_required", "Ask the workspace operator to configure sign-in.", 503)
    oidc_url(settings.oidc_redirect_uri)
    issuer = oidc_url(settings.oidc_issuer_url)
    config = await provider_json(client, "GET", issuer.rstrip("/") + "/.well-known/openid-configuration")
    if config.get("issuer") != issuer:
        raise AuthorityError("identity_provider_error", "The identity issuer does not match the trusted configuration.", 502)
    for key in ["authorization_endpoint", "token_endpoint", "jwks_uri"]:
        oidc_url(config.get(key, ""))
    return config


def validate_id_token(token, jwks, nonce, *, access_token=None, code=None):
    settings = get_settings()
    try:
        header = jwt.get_unverified_header(token)
        if header.get("crit"):
            raise ValueError("Unsupported critical token header")
        if header.get("alg") != "RS256" or not isinstance(header.get("kid"), str):
            raise ValueError("Unsupported signing key")
        material = jwks.get("keys", [])
        if not isinstance(material, list) or len(material) > 100:
            raise ValueError("Invalid signing key set")
        keys = [key for key in material if isinstance(key, dict) and key.get("kid") == header["kid"] and key.get("kty") == "RSA"
                and key.get("use", "sig") == "sig" and key.get("alg", "RS256") == "RS256"
                and "verify" in key.get("key_ops", ["verify"])]
        if len(keys) != 1:
            raise ValueError("Signing key is missing or ambiguous")
        claims = jwt.decode(token, jwt.PyJWK.from_dict(keys[0]).key, algorithms=["RS256"],
            issuer=settings.oidc_issuer_url, audience=settings.oidc_client_id, leeway=30,
            options={"require": ["iss", "sub", "aud", "exp", "iat", "nonce"]})
        if not isinstance(claims["sub"], str) or not claims["sub"] or len(claims["sub"]) > 255:
            raise ValueError("Invalid subject")
        if not isinstance(claims["nonce"], str) or not secrets.compare_digest(claims["nonce"], nonce):
            raise ValueError("Nonce mismatch")
        multiple_audiences = isinstance(claims["aud"], list) and len(claims["aud"]) > 1
        if multiple_audiences or "azp" in claims:
            if claims.get("azp") != settings.oidc_client_id:
                raise ValueError("Authorized party mismatch")
        for name, value in (("at_hash", access_token), ("c_hash", code)):
            if name in claims:
                expected = base64.urlsafe_b64encode(hashlib.sha256(value.encode()).digest()[:16]).rstrip(b"=").decode() if isinstance(value, str) else ""
                if not expected or not secrets.compare_digest(claims[name], expected):
                    raise ValueError("Token binding mismatch")
        return claims
    except (jwt.PyJWTError, ValueError, TypeError, KeyError) as exc:
        raise AuthorityError("invalid_identity_token", "Sign-in could not be verified. Start sign-in again.", 401) from exc


class IdentityService:
    def __init__(self, db):
        self.db = db

    async def context(self, principal: Principal, *, actor=None, session=None, source="rest"):
        membership = await self.db.get(WorkspaceMembership, principal.id)
        projects = (await self.db.scalars(select(ProjectMembership).where(ProjectMembership.principal_id == principal.id))).all()
        link = await self.db.get(PrincipalProfileLink, principal.id)
        return Authority(principal.id, principal.kind, membership.role if membership else None,
            {item.project_id: item.role for item in projects}, actor_id=actor.id if actor else principal.agent_actor_id,
            actor_role=actor.role if actor else None, session_id=session.id if session else None,
            profile_id=link.profile_id if link else getattr(actor, "profile_id", None), source=source,
            local=get_settings().workchord_auth_mode == "trusted_local",
            scopes=frozenset(json.loads(actor.scopes)) if actor else frozenset())

    async def actor_context(self, actor, *, source="rest"):
        with internal_authority(self.db):
            principal = await self.db.scalar(select(Principal).where(Principal.agent_actor_id == actor.id))
            if principal is None:
                require_identity_writes()
                principal = Principal(kind="agent", display_name=actor.display_name, agent_actor_id=actor.id)
                self.db.add(principal)
                await self.db.flush()
            if not principal.enabled:
                raise AuthorityError("authentication_required", "This identity is disabled.", 401)
            return await self.context(principal, actor=actor, source=source)

    @atomic_command
    async def begin_login(self, return_path="/"):
        require_identity_writes()
        async with httpx.AsyncClient(timeout=10, follow_redirects=False) as client:
            provider = await provider_configuration(client)
        state, browser, nonce, verifier = [secrets.token_urlsafe(32) for _ in range(4)]
        with internal_authority(self.db):
            self.db.add(OIDCLoginAttempt(state_hash=digest(state), browser_hash=digest(browser), nonce=nonce,
                verifier=verifier, return_path=safe_return_path(return_path), expires_at=utc_now() + timedelta(minutes=10)))
            await self.db.flush()
        query = {"client_id": get_settings().oidc_client_id, "redirect_uri": get_settings().oidc_redirect_uri,
                 "response_type": "code", "scope": "openid profile", "state": state, "nonce": nonce,
                 "code_challenge": base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode(),
                 "code_challenge_method": "S256"}
        return provider["authorization_endpoint"] + ("&" if "?" in provider["authorization_endpoint"] else "?") + urlencode(query), browser

    @atomic_command
    async def finish_login(self, code, state, browser, *, ip_address, user_agent):
        require_identity_writes()
        with internal_authority(self.db):
            attempt = await self.db.get(OIDCLoginAttempt, digest(state))
            if attempt is None or attempt.consumed_at is not None or as_utc(attempt.expires_at) <= utc_now() or not browser or not secrets.compare_digest(attempt.browser_hash, digest(browser)):
                raise AuthorityError("invalid_login_state", "Sign-in expired or belongs to another browser. Start again.", 401)
            used = await self.db.execute(update(OIDCLoginAttempt).where(OIDCLoginAttempt.state_hash == attempt.state_hash,
                OIDCLoginAttempt.consumed_at.is_(None)).values(consumed_at=utc_now()).execution_options(synchronize_session=False))
            if used.rowcount != 1:
                raise AuthorityError("invalid_login_state", "This sign-in attempt has already been used.", 401)
            async with httpx.AsyncClient(timeout=10, follow_redirects=False) as client:
                provider = await provider_configuration(client)
                payload = {"grant_type": "authorization_code", "code": code, "client_id": get_settings().oidc_client_id,
                           "redirect_uri": get_settings().oidc_redirect_uri, "code_verifier": attempt.verifier}
                if get_settings().oidc_client_secret:
                    payload["client_secret"] = get_settings().oidc_client_secret
                tokens = await provider_json(client, "POST", provider["token_endpoint"], data=payload)
                jwks = await provider_json(client, "GET", provider["jwks_uri"])
            claims = validate_id_token(tokens.get("id_token", ""), jwks, attempt.nonce,
                                       access_token=tokens.get("access_token"), code=code)
            subject = await self.db.scalar(select(IdentitySubject).where(IdentitySubject.issuer == claims["iss"], IdentitySubject.subject == claims["sub"]))
            if subject is None:
                try:
                    async with self.db.begin_nested():
                        principal = Principal(kind="human", display_name=str(claims.get("name") or "Member")[:255])
                        self.db.add(principal)
                        await self.db.flush()
                        subject = IdentitySubject(principal_id=principal.id, issuer=claims["iss"], subject=claims["sub"])
                        self.db.add(subject)
                        await self.db.flush()
                except IntegrityError:
                    subject = await self.db.scalar(select(IdentitySubject).where(IdentitySubject.issuer == claims["iss"], IdentitySubject.subject == claims["sub"]))
                    if subject is None:
                        raise
            principal = await self.db.get(Principal, subject.principal_id)
            if not principal.enabled or principal.kind != "human":
                raise AuthorityError("authentication_required", "This identity is disabled.", 401)
            session, raw = await self.issue_session(principal.id, ip_address, user_agent)
            attempt.verifier = attempt.nonce = "consumed"
            return session, raw, attempt.return_path

    async def issue_session(self, principal_id, ip_address, user_agent):
        require_identity_writes()
        raw = secrets.token_urlsafe(32)
        with internal_authority(self.db):
            session = UserSession(principal_id=principal_id, session_token_hash=digest(raw),
                csrf_token=secrets.token_urlsafe(32), authenticated_at=utc_now(),
                ip_address=ip_address[:128], user_agent=(user_agent or "")[:512],
                expires_at=utc_now() + timedelta(seconds=get_settings().auth_session_max_age_seconds))
            self.db.add(session)
            await self.db.flush()
        return session, raw

    @atomic_command
    async def transfer_guest(self, raw_token, principal_id, *, operator_reason=None, guest_id=None):
        require_identity_writes()
        authority = self.db.info.get("authority")
        if authority is None or authority.principal_id is None:
            raise AuthorityError("authentication_required", "Sign in before transferring personal data.", 401)
        if guest_id is not None:
            require_operator(self.db)
            if not operator_reason or len(operator_reason.strip()) < 8:
                raise AuthorityError("recovery_reason_required", "Explain the ownership recovery decision.", 422)
        elif principal_id != authority.principal_id:
            raise AuthorityError()
        from app.models.saved_view import SavedView
        from app.models.plan_share import PlanShare
        with internal_authority(self.db):
            guest = await self.db.scalar(select(UserSession).where(
                UserSession.id == guest_id if guest_id is not None else UserSession.session_token_hash == digest(raw_token or "")
            ).with_for_update())
            if guest is None or guest.principal_id is not None:
                raise AuthorityError("guest_proof_required", "A valid guest session or operator recovery is required.", 403)
            transfer = await self.db.get(OwnershipTransfer, guest.id)
            if transfer is not None:
                if transfer.principal_id != principal_id:
                    raise AuthorityError()
                return {"transferred": False, "already_transferred": True}
            if guest_id is None and (guest.revoked_at is not None or guest.expires_at is None or as_utc(guest.expires_at) <= utc_now()):
                raise AuthorityError("guest_proof_expired", "This guest token can no longer prove ownership.", 403)
            target = await self.db.get(Principal, principal_id)
            if target is None or target.kind != "human" or not target.enabled:
                raise AuthorityError()
            views = await self.db.execute(update(SavedView).where(SavedView.created_by_session_id == guest.id, SavedView.owner_principal_id.is_(None)).values(owner_principal_id=principal_id))
            shares = (await self.db.scalars(select(PlanShare).where(PlanShare.created_by_session_id == guest.id, PlanShare.owner_principal_id.is_(None)))).all()
            for share in shares:
                share.owner_principal_id = principal_id
                share.public_id = secrets.token_urlsafe(24)
            reason = operator_reason or "Owner proved the current guest token and explicitly requested transfer"
            self.db.add(OwnershipTransfer(guest_session_id=guest.id, principal_id=principal_id,
                authorized_by_principal_id=authority.principal_id, reason=reason))
            guest.revoked_at = utc_now()
            self.db.add(CommandAudit(principal_id=authority.principal_id, action="guest_ownership_transferred", source=authority.source,
                correlation_id=authority.correlation_id, reason=reason,
                details={"guest_session_id": guest.id, "principal_id": principal_id, "view_count": views.rowcount, "rotated_share_count": len(shares)}))
            await self.db.flush()
            return {"transferred": True, "view_count": views.rowcount, "rotated_share_count": len(shares)}

    @atomic_command
    async def cleanup_sessions(self, *, limit=100):
        require_operator(self.db)
        require_identity_writes()
        if not 1 <= limit <= 500:
            raise ValueError("Cleanup limit must be between 1 and 500")
        from sqlalchemy import or_, and_
        cutoff = utc_now() - timedelta(days=get_settings().session_metadata_retention_days)
        with internal_authority(self.db):
            rows = (await self.db.scalars(select(UserSession).where(
                or_(UserSession.expires_at <= cutoff, UserSession.revoked_at <= cutoff,
                    and_(UserSession.expires_at.is_(None), UserSession.last_seen_at <= cutoff)),
                or_(UserSession.ip_address != "redacted", UserSession.user_agent.is_not(None), UserSession.session_token_hash.is_not(None)))
                .order_by(UserSession.id).limit(limit))).all()
            for row in rows:
                row.ip_address, row.user_agent, row.session_token_hash, row.csrf_token = "redacted", None, None, None
                row.revoked_at = row.revoked_at or utc_now()
            expired_attempts = (await self.db.scalars(select(OIDCLoginAttempt).where(OIDCLoginAttempt.expires_at <= utc_now()).order_by(OIDCLoginAttempt.expires_at).limit(limit))).all()
            for attempt in expired_attempts:
                await self.db.delete(attempt)
            await self.db.flush()
            return {"anonymized": len(rows), "expired_login_attempts_removed": len(expired_attempts), "limit": limit, "references_preserved": True}


async def bind_verified_system(db, *, source, reason):
    """Bind an integration only after its server-owned credential has been verified."""
    if db.info.get("authority") is not None:
        return
    with internal_authority(db):
        state = await db.get(WorkspaceAuthorityState, 1)
        if state is None or state.operator_principal_id is None:
            if get_settings().workchord_auth_mode == "trusted_local":
                return
            raise AuthorityError("identity_migration_required", "Apply the identity migration before running integrations.", 503)
        principal = await db.get(Principal, state.operator_principal_id)
        if principal is None or not principal.enabled:
            raise AuthorityError("authentication_required", "The integration authority is disabled.", 401)
        db.info["authority"] = Authority(principal.id, "system", workspace_role="operator", source=source, reason=reason)


async def initialize_control_plane(db):
    """Seed the control-plane principal during explicit post-migration repair, never schema-only bootstrap."""
    require_identity_writes()
    with internal_authority(db):
        state = await db.get(WorkspaceAuthorityState, 1)
        if state is not None:
            return state.operator_principal_id
        principal = Principal(kind="system", display_name="Operator API", enabled=True)
        db.add(principal)
        await db.flush()
        db.add(WorkspaceAuthorityState(id=1, operator_principal_id=principal.id))
        await db.flush()
        return principal.id
