"""One policy for the source link carried by intakes and tasks.

A source link is shown to people and never fetched by the server, so it may be:

* an absolute public ``http(s)`` URL, kept as written;
* a path inside this WorkChord instance (``/tasks?project=6``), kept as written;
* an absolute URL that points at this same instance, which is rewritten to its
  relative path so it keeps working wherever the instance is opened.

Anything else (private, link-local or reserved addresses, other schemes, embedded
credentials) is refused. "This same instance" means a loopback host (``localhost``,
``*.localhost``, ``127.0.0.0/8``, ``::1``, on any port) or the host and port of the
configured ``PUBLIC_BASE_URL``.
"""
from __future__ import annotations

import ipaddress
from dataclasses import dataclass
from typing import Literal, Optional
from urllib.parse import urlparse

from app.config import get_settings
from app.utils.url_policy import URLPolicyError, normalize_stored_display_url

SOURCE_LINK_ERROR_CODE = "intake_source_link_not_allowed"
SOURCE_LINK_FIELD = "source_url"
SOURCE_LINK_NEXT_STEP = (
    "Use a public http(s) link, a path inside this instance such as /tasks?project=1, "
    "or clear the source link."
)

SourceLinkAction = Literal["none", "kept", "rewritten", "dropped"]


class SourceLinkRefused(ValueError):
    """Raised when a source link breaks the policy; carries a stable, named error."""

    code = SOURCE_LINK_ERROR_CODE
    field = SOURCE_LINK_FIELD

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(f"Source link is not allowed: {reason}")

    def detail(self) -> dict[str, str]:
        return {
            "code": self.code,
            "field": self.field,
            "message": str(self),
            "next_step": SOURCE_LINK_NEXT_STEP,
        }


@dataclass(frozen=True)
class SourceLinkDecision:
    """What the policy does with one source link."""

    action: SourceLinkAction
    original: Optional[str]
    value: Optional[str]
    reason: Optional[str] = None

    def message(self) -> Optional[str]:
        if self.action == "rewritten":
            return (
                "The source link pointed at this instance and was carried over "
                f"as the relative path {self.value}."
            )
        if self.action == "dropped":
            return f"The source link was not carried over ({self.reason}). It stays on the intake."
        return None


def _default_port(scheme: str) -> int | None:
    return {"http": 80, "https": 443}.get(scheme)


def _instance_authorities() -> set[tuple[str, int | None]]:
    base = (get_settings().public_base_url or "").strip()
    if not base:
        return set()
    parsed = urlparse(base)
    if not parsed.hostname:
        return set()
    return {(parsed.hostname.lower().rstrip("."), parsed.port or _default_port(parsed.scheme))}


def _is_loopback_host(host: str) -> bool:
    if host == "localhost" or host.endswith(".localhost"):
        return True
    try:
        return ipaddress.ip_address(host.strip("[]")).is_loopback
    except ValueError:
        return False


def _is_instance_path(value: str) -> bool:
    return (
        value.startswith("/")
        and not value.startswith("//")
        and "\\" not in value
        and not any(ch.isspace() or ord(ch) < 32 for ch in value)
    )


def evaluate_source_link(raw: Optional[str]) -> SourceLinkDecision:
    """Decide what happens to a source link without raising."""
    if raw is None or not str(raw).strip():
        return SourceLinkDecision("none", raw, None)
    value = str(raw).strip()
    if _is_instance_path(value):
        return SourceLinkDecision("kept", raw, value)
    parsed = urlparse(value)
    host = (parsed.hostname or "").lower().rstrip(".")
    if parsed.scheme in {"http", "https"} and host and not (parsed.username or parsed.password):
        try:
            port = parsed.port
        except ValueError:
            return SourceLinkDecision("dropped", raw, None, "the address has an invalid port")
        if _is_loopback_host(host) or (host, port or _default_port(parsed.scheme)) in _instance_authorities():
            relative = (parsed.path or "/") + (f"?{parsed.query}" if parsed.query else "")
            if parsed.fragment:
                relative += f"#{parsed.fragment}"
            if not _is_instance_path(relative):
                return SourceLinkDecision("dropped", raw, None, "the address of this instance has a path that cannot be kept as a relative link")
            return SourceLinkDecision("rewritten", raw, relative)
    try:
        return SourceLinkDecision("kept", raw, normalize_stored_display_url(value))
    except URLPolicyError as exc:
        return SourceLinkDecision("dropped", raw, None, str(exc).rstrip("."))


def normalize_source_link(raw: Optional[str]) -> Optional[str]:
    """Return the link to store, or raise ``SourceLinkRefused``."""
    decision = evaluate_source_link(raw)
    if decision.action == "dropped":
        raise SourceLinkRefused(decision.reason or "the address is not allowed")
    return decision.value
