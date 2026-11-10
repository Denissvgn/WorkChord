# url_policy Module

**Path:** `backend/app/utils/url_policy.py`

## Description

Centralized outbound URL and host validation.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.config` | `get_settings` |
| `ipaddress` | `ipaddress` |
| `socket` | `socket` |
| `urllib.parse` | `urlparse` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/utils/url_policy.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/url_policy.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (11) |
| Outbound | `backend` (1) |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [URLPolicyError](../entities/URLPolicyError.md) | 14 | `ValueError` | Raised when a URL or host violates outbound egress policy. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_is_blocked_ip` | `(ip: IPAddress) -> bool` | — | — |
| `_literal_ip` | `(host: str) -> IPAddress \| None` | — | — |
| `_host_looks_local` | `(host: str) -> bool` | — | — |
| `validate_public_host` | `(host: str, *, allow_private: bool = False, resolve: bool = True) -> str` | — | Validate a hostname or IP literal for outbound network use. |
| `normalize_external_http_url` | `(value: str, *, require_https: bool = False, allow_http_localhost: bool = False, allow_http_private: bool = False, resolve: bool = True) -> str` | — | Normalize and validate an outbound HTTP(S) URL. |
| `normalize_provider_api_url` | `(value: str) -> str` | — | Validate a provider API URL that may carry credentials in headers. |
| `normalize_stored_display_url` | `(value: str) -> str` | — | Validate externally displayed user-supplied links before persistence. |
