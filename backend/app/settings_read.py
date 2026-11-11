"""Read-only settings for people without the admin key.

Workspace members and trusted-local sessions may read the settings that explain
how the workspace behaves. Every change still needs the admin key. Values that
are not secrets but are still sensitive are withheld from these readers:
endpoint URLs are reduced to their host, and the mail host and login, webhook
header values, and delivery response bodies and errors are left out. Secrets
are never returned to anyone; responses only say whether one is set.
"""

from typing import Annotated, Optional
from urllib.parse import urlsplit

from fastapi import Header, Request

from app.security import ADMIN_API_KEY_HEADER, require_admin_api_key

READABLE_SETTINGS_PATHS = frozenset({
    "/system-settings", "/email-settings", "/scheduling-rules",
    "/outbound-webhooks/targets", "/outbound-webhooks/deliveries", "/github/status-automation-rules",
})


def settings_reader(authority) -> bool:
    """A person who may read settings without the admin key."""
    return authority is not None and (authority.local or authority.kind == "human" and authority.workspace_role is not None)


def withholds(authority) -> bool:
    """Whether a settings response must leave out sensitive values."""
    return authority is None or not authority.operator


def host_only(url: str | None) -> str:
    try:
        return urlsplit(url or "").hostname or ""
    except ValueError:
        return ""


async def require_settings_access(
    request: Request,
    api_key: Annotated[Optional[str], Header(alias=ADMIN_API_KEY_HEADER)] = None,
) -> None:
    """Let settings readers read; every other request needs the admin key."""
    if request.method in {"GET", "HEAD"} and settings_reader(getattr(request.state, "authority", None)):
        return
    await require_admin_api_key(api_key, request)


def redact_system_settings(response):
    response.llm.api_url = host_only(response.llm.api_url)
    response.github.api_url = host_only(response.github.api_url)
    response.redacted_fields = ["llm.api_url", "github.api_url"]
    return response


def redact_email_settings(response):
    return response.model_copy(update={"smtp_host": "", "smtp_user": "", "redacted_fields": ["smtp_host", "smtp_user"]})


def redact_webhook_target(response):
    return response.model_copy(update={"url": host_only(response.url), "headers_json": {name: "" for name in response.headers_json},
                                       "redacted_fields": ["url", "headers_json"]})


def redact_webhook_delivery(response):
    return response.model_copy(update={"target_url": host_only(response.target_url), "last_error": None, "last_response_body": None,
                                       "event": response.event.model_copy(update={"payload_json": {}}),
                                       "redacted_fields": ["target_url", "last_error", "last_response_body", "event.payload_json"]})
