"""Shared request authorization helpers."""
from typing import Annotated, Optional
import secrets

from fastapi import Header, HTTPException, status

from app.config import get_settings

ADMIN_API_KEY_HEADER = "X-Admin-API-Key"


def admin_api_key_is_valid(api_key: Optional[str]) -> bool:
    """Return whether a provided admin API key matches configured settings."""
    configured = get_settings().workchord_admin_api_key
    if not configured or not api_key:
        return False
    return secrets.compare_digest(api_key, configured)


async def require_admin_api_key(
    api_key: Annotated[Optional[str], Header(alias=ADMIN_API_KEY_HEADER)] = None,
) -> None:
    """Require the configured admin API key for control-plane API routes."""
    if not get_settings().workchord_admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin API key is not configured.",
        )
    if not admin_api_key_is_valid(api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Missing or invalid {ADMIN_API_KEY_HEADER} header.",
        )
