"""Explicit browser consent and one-use proof-bound native authentication."""

import base64
from datetime import timedelta
import hashlib
import secrets
from urllib.parse import urlencode

from sqlalchemy import delete, func, select, update

from app.authority import AuthorityError, internal_authority
from app.commands import atomic_command
from app.config import get_settings
from app.models.identity import Principal
from app.models.native_connection import NativeConnection
from app.models.user_session import UserSession
from app.services.identity_service import IdentityService, digest, require_identity_writes
from app.utils.time import as_utc, utc_now


class NativeSessionService:
    def __init__(self, db):
        self.db = db

    def human(self):
        authority = self.db.info.get("authority")
        if authority is None or authority.kind != "human" or authority.session_id is None:
            raise AuthorityError("human_session_required", "Sign in with a human account to connect a device.", 403)
        return authority

    async def connection(self, request_id):
        row = await self.db.get(NativeConnection, digest(request_id))
        if row is None:
            raise AuthorityError("native_connection_unavailable", "Start a new connection from your device.", 404)
        if as_utc(row.expires_at) <= utc_now() or row.consumed_at is not None:
            raise AuthorityError("native_connection_expired", "This connection has ended. Start again on your device.", 410)
        return row

    @atomic_command
    async def start(self, code_challenge, ip_address):
        require_identity_writes()
        if get_settings().workchord_auth_mode != "managed":
            raise AuthorityError("native_auth_unavailable", "Native sign-in requires a managed workspace.", 409)
        now = utc_now()
        ip_hash = digest(ip_address)
        with internal_authority(self.db):
            expired = select(NativeConnection.request_hash).where(NativeConnection.expires_at <= now).limit(100)
            await self.db.execute(delete(NativeConnection).where(NativeConnection.request_hash.in_(expired)))
            counts = await self.db.scalar(select(func.count()).select_from(NativeConnection).where(
                NativeConnection.expires_at > now, NativeConnection.request_ip_hash == ip_hash))
            total = await self.db.scalar(select(func.count()).select_from(NativeConnection).where(NativeConnection.expires_at > now))
            if counts >= 32 or total >= 4096:
                raise AuthorityError("native_connection_limit", "Too many connection attempts. Try again later.", 429)
            request_id = secrets.token_urlsafe(32)
            code = "".join(secrets.choice("ABCDEFGHJKLMNPQRSTUVWXYZ23456789") for _ in range(8))
            code = code[:4] + "-" + code[4:]
            expires = now + timedelta(minutes=10)
            self.db.add(NativeConnection(request_hash=digest(request_id), code_challenge=code_challenge,
                verification_code=code, request_ip_hash=ip_hash, expires_at=expires))
        return {"request_id": request_id, "verification_code": code, "expires_at": expires,
                "verification_path": "/mobile/connect?" + urlencode({"request": request_id})}

    async def describe(self, request_id):
        self.human()
        with internal_authority(self.db):
            row = await self.connection(request_id)
            return {"verification_code": row.verification_code, "expires_at": row.expires_at,
                    "approved": row.approved_session_id is not None}

    @atomic_command
    async def approve(self, request_id, verification_code):
        require_identity_writes()
        authority = self.human()
        with internal_authority(self.db):
            row = await self.connection(request_id)
            if not secrets.compare_digest(row.verification_code, verification_code):
                raise AuthorityError("native_code_mismatch", "Compare the code with your device before approving.", 422)
            if row.approved_session_id is not None:
                if row.approved_session_id != authority.session_id:
                    raise AuthorityError("native_connection_already_approved", "This connection already belongs to another session.", 409)
                return {"approved": True}
            changed = await self.db.execute(update(NativeConnection).where(
                NativeConnection.request_hash == row.request_hash, NativeConnection.approved_session_id.is_(None),
                NativeConnection.consumed_at.is_(None), NativeConnection.expires_at > utc_now())
                .values(approved_session_id=authority.session_id))
            if changed.rowcount != 1:
                raise AuthorityError("native_connection_changed", "This connection changed. Reload before approving.", 409)
        return {"approved": True}

    @atomic_command
    async def exchange(self, request_id, code_verifier, ip_address, user_agent):
        require_identity_writes()
        with internal_authority(self.db):
            row = await self.db.get(NativeConnection, digest(request_id))
            challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b"=").decode()
            if row is None or not secrets.compare_digest(row.code_challenge, challenge):
                raise AuthorityError("native_connection_unavailable", "Start a new connection from your device.", 404)
            await self.connection(request_id)
            if row.approved_session_id is None:
                return {"status": "pending"}
            source = await self.db.get(UserSession, row.approved_session_id)
            principal = await self.db.scalar(select(Principal).where(Principal.id == source.principal_id).with_for_update()) if source else None
            source = await self.db.scalar(select(UserSession).where(UserSession.id == row.approved_session_id)
                .with_for_update().execution_options(populate_existing=True))
            if (source is None or source.revoked_at is not None or source.expires_at is None
                    or as_utc(source.expires_at) <= utc_now() or principal is None
                    or not principal.enabled or principal.kind != "human"):
                raise AuthorityError("native_approval_revoked", "Sign in again in the browser before connecting.", 401)
            consumed = await self.db.execute(update(NativeConnection).where(
                NativeConnection.request_hash == row.request_hash, NativeConnection.consumed_at.is_(None),
                NativeConnection.expires_at > utc_now()).values(consumed_at=utc_now()))
            if consumed.rowcount != 1:
                raise AuthorityError("native_connection_expired", "This connection has ended. Start again on your device.", 410)
            session, raw = await IdentityService(self.db).issue_session(principal.id, ip_address, user_agent)
        return {"access_token": raw, "token_type": "Bearer", "expires_at": session.expires_at}
