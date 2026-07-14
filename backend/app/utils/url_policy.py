"""Centralized outbound URL and host validation."""
from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse

from app.config import get_settings

PRIVATE_HOST_SENTINELS = {"localhost", "localhost.localdomain"}
IPAddress = ipaddress.IPv4Address | ipaddress.IPv6Address


class URLPolicyError(ValueError):
    """Raised when a URL or host violates outbound egress policy."""


def _is_blocked_ip(ip: IPAddress) -> bool:
    return (
        ip.is_loopback
        or ip.is_private
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_reserved
        or ip.is_unspecified
    )


def _literal_ip(host: str) -> IPAddress | None:
    value = host.strip("[]")
    try:
        return ipaddress.ip_address(value)
    except ValueError:
        return None


def _host_looks_local(host: str) -> bool:
    lowered = host.lower().rstrip(".")
    return lowered in PRIVATE_HOST_SENTINELS or lowered.endswith(".localhost")


def validate_public_host(host: str, *, allow_private: bool = False, resolve: bool = True) -> str:
    """Validate a hostname or IP literal for outbound network use."""
    normalized = host.strip().lower().rstrip(".")
    if not normalized:
        raise URLPolicyError("Host is required.")
    if "://" in normalized or "@" in normalized or "/" in normalized:
        raise URLPolicyError("Host must not include a scheme, credentials, or path.")
    if allow_private:
        return normalized
    if _host_looks_local(normalized):
        raise URLPolicyError("Localhost targets are not allowed.")

    literal = _literal_ip(normalized)
    if literal is not None:
        if _is_blocked_ip(literal):
            raise URLPolicyError("Private, local, or reserved IP targets are not allowed.")
        return normalized

    if resolve:
        try:
            infos = socket.getaddrinfo(normalized, None, type=socket.SOCK_STREAM)
        except socket.gaierror as exc:
            raise URLPolicyError(f"Host could not be resolved: {normalized}") from exc
        for info in infos:
            resolved_ip = ipaddress.ip_address(info[4][0])
            if _is_blocked_ip(resolved_ip):
                raise URLPolicyError("Host resolves to a private, local, or reserved IP address.")

    return normalized


def normalize_external_http_url(
    value: str,
    *,
    require_https: bool = False,
    allow_http_localhost: bool = False,
    allow_http_private: bool = False,
    resolve: bool = True,
) -> str:
    """Normalize and validate an outbound HTTP(S) URL."""
    parsed = urlparse(str(value).strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise URLPolicyError("URL must be an absolute http(s) URL.")
    if parsed.username or parsed.password:
        raise URLPolicyError("URL credentials are not allowed.")
    host = parsed.hostname
    if not host:
        raise URLPolicyError("URL host is required.")

    literal = _literal_ip(host)
    explicit_private_host = _host_looks_local(host) or (
        literal is not None and _is_blocked_ip(literal)
    )
    allow_insecure_target = (
        allow_http_localhost and _host_looks_local(host)
    ) or (allow_http_private and explicit_private_host)
    if require_https and parsed.scheme != "https" and not allow_insecure_target:
        raise URLPolicyError("URL must use HTTPS.")

    allow_private = get_settings().allow_private_egress_urls
    if allow_http_localhost and parsed.scheme == "http" and _host_looks_local(host):
        allow_private = True
    validate_public_host(host, allow_private=allow_private, resolve=resolve)
    return parsed.geturl()


def normalize_provider_api_url(value: str) -> str:
    """Validate a provider API URL that may carry credentials in headers."""
    settings = get_settings()
    return normalize_external_http_url(
        value,
        require_https=True,
        allow_http_private=settings.allow_private_egress_urls,
        resolve=False,
    )


def normalize_stored_display_url(value: str) -> str:
    """Validate externally displayed user-supplied links before persistence."""
    return normalize_external_http_url(value, require_https=False, resolve=False)
