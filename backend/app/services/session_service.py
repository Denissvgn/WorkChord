"""Opaque browser-session resolution and trusted request audit metadata."""

from datetime import timedelta
import hashlib
from ipaddress import ip_address, ip_network
import re
import secrets
from typing import Annotated, Optional

from fastapi import Depends, Request, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.maintenance import MaintenanceModeError
from app.models.user_session import UserSession
from app.runtime_telemetry import metrics
from app.utils.time import as_utc, utc_now


_SESSION_TOKEN_PATTERN = re.compile(r"^[A-Za-z0-9_-]{43,128}$")


def _token_digest(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _new_token() -> str:
    return secrets.token_urlsafe(32)


def _cookie_options() -> dict:
    settings = get_settings()
    return {
        "key": settings.session_cookie_name,
        "max_age": settings.session_max_age_seconds,
        "httponly": True,
        "secure": settings.session_cookie_secure,
        "samesite": "lax",
        "path": settings.api_prefix or "/api",
    }


async def get_client_ip(request: Request) -> str:
    """Read proxy client metadata only from explicitly trusted immediate peers."""
    direct_ip = request.client.host if request.client else "unknown"
    try:
        peer = ip_address(direct_ip)
        trusted = any(
            peer in ip_network(network, strict=False)
            for network in get_settings().trusted_proxy_ips
        )
    except ValueError:
        trusted = False
    if trusted:
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()
    return direct_ip


async def _get_session_by_token(
    db: AsyncSession,
    token: str | None,
) -> UserSession | None:
    if not token or not _SESSION_TOKEN_PATTERN.fullmatch(token):
        return None
    result = await db.execute(
        select(UserSession).where(UserSession.session_token_hash == _token_digest(token))
    )
    session = result.scalar_one_or_none()
    if not session or session.revoked_at is not None:
        return None
    if session.expires_at is not None and as_utc(session.expires_at) <= utc_now():
        # Expiry is already fail-closed. Do not manufacture a hidden GET write;
        # explicit cleanup can mark old rows revoked outside request handling.
        return None
    return session


async def _create_session(
    db: AsyncSession,
    ip_address: str,
    user_agent: str | None,
) -> tuple[UserSession, str]:
    """Create an isolated session, retrying the vanishingly rare unique collision."""
    settings = get_settings()
    for _attempt in range(3):
        raw_token = _new_token()
        session = UserSession(
            public_id=secrets.token_hex(6),
            session_token_hash=_token_digest(raw_token),
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=utc_now() + timedelta(seconds=settings.session_max_age_seconds),
        )
        db.add(session)
        try:
            await db.commit()
            await db.refresh(session)
            return session, raw_token
        except IntegrityError:
            await db.rollback()
    raise RuntimeError("Unable to allocate a unique browser session")


async def get_or_create_session(
    db: AsyncSession,
    ip_address: str,
    user_agent: Optional[str] = None,
    session_token: str | None = None,
) -> tuple[UserSession, str]:
    """Resolve an opaque token or create a fresh session without IP ownership."""
    session = await _get_session_by_token(db, session_token)
    if session is None:
        mode = get_settings().maintenance_mode
        if mode != "off":
            raise MaintenanceModeError(
                operation="browser session creation",
                mode=mode,
            )
        return await _create_session(db, ip_address, user_agent)

    now = utc_now()
    settings = get_settings()
    if settings.maintenance_mode != "off":
        return session, session_token

    last_seen = as_utc(session.last_seen_at)
    touch_due = now - last_seen >= timedelta(
        seconds=settings.session_touch_interval_seconds
    )
    metadata_changed = (
        session.ip_address != ip_address
        or (user_agent is not None and session.user_agent != user_agent)
    )
    if touch_due or metadata_changed:
        session.last_seen_at = now
        session.expires_at = now + timedelta(seconds=settings.session_max_age_seconds)
        if session.ip_address != ip_address:
            session.ip_address = ip_address
        if user_agent is not None and session.user_agent != user_agent:
            session.user_agent = user_agent
        await db.commit()
        await db.refresh(session)
        metrics.increment("workchord_browser_session_touches_total")
    else:
        metrics.increment("workchord_browser_session_touch_skips_total")
    return session, session_token


async def get_current_session(
    request: Request,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserSession:
    """FastAPI dependency resolving the current browser and refreshing its cookie."""
    settings = get_settings()
    session, raw_token = await get_or_create_session(
        db=db,
        ip_address=await get_client_ip(request),
        user_agent=request.headers.get("User-Agent"),
        session_token=request.cookies.get(settings.session_cookie_name),
    )
    response.set_cookie(value=raw_token, **_cookie_options())
    return session


async def rotate_session(
    db: AsyncSession,
    session: UserSession,
    response: Response,
) -> UserSession:
    """Rotate a raw token while preserving ownership links on the session row."""
    raw_token = _new_token()
    session.session_token_hash = _token_digest(raw_token)
    session.expires_at = utc_now() + timedelta(
        seconds=get_settings().session_max_age_seconds
    )
    session.revoked_at = None
    await db.commit()
    await db.refresh(session)
    response.set_cookie(value=raw_token, **_cookie_options())
    return session


async def revoke_session(
    db: AsyncSession,
    session: UserSession,
    response: Response,
) -> None:
    """Revoke the current browser identity and remove its cookie."""
    session.revoked_at = utc_now()
    await db.commit()
    options = _cookie_options()
    response.delete_cookie(
        key=options["key"],
        path=options["path"],
        secure=options["secure"],
        httponly=True,
        samesite="lax",
    )


async def get_session_by_ip(db: AsyncSession, ip_address: str) -> Optional[UserSession]:
    """Return the latest audit match; IP must never be used for authorization."""
    result = await db.execute(
        select(UserSession)
        .where(UserSession.ip_address == ip_address)
        .order_by(UserSession.id.desc())
    )
    return result.scalars().first()
