# test_mcp_proxy_host_header Module

**Path:** `backend/tests/test_mcp_proxy_host_header.py`

## Description

The stock frontend proxy must forward MCP requests with the client's Host port.

The MCP host guard matches the default allowlist (localhost:*, 127.0.0.1:*,
[::1]:*) on the port. nginx's $host drops the port, so the MCP location must
forward $http_host. The round-trip test runs the real frontend/nginx.conf in
nginx, with a stub backend that echoes the Host it receives, and feeds that
forwarded value through the real MCPHostValidationMiddleware.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.mcp_server` | `MCPHostValidationMiddleware` |
| `asyncio` | `asyncio` |
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `re` | `re` |
| `shutil` | `shutil` |
| `subprocess` | `subprocess` |
| `time` | `time` |
| `urllib.error` | `urllib.error` |
| `urllib.request` | `urllib.request` |
| `uuid` | `uuid` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_server.py"]
    n1["backend/tests/test_mcp_proxy_host_header.py"]
    n1 --> n0
    click n0 "../modules/mcp_server.md"
    click n1 "../modules/test_mcp_proxy_host_header.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [mcp_server](../modules/mcp_server.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_nginx_image` | `() -> str` | — | — |
| `_location_block` | `(config: str, header: str) -> str` | — | — |
| `test_mcp_location_forwards_host_with_port_and_precedes_api_prefix` | `() -> None` | — | — |
| `_guard_status` | `(host: str) -> int` | — | — |
| `test_host_guard_accepts_default_loopback_hosts_on_non_default_port` | `() -> None` | — | — |
| `test_host_guard_rejects_host_outside_allowlist` | `() -> None` | — | — |
| `_docker_available` | `() -> bool` | — | — |
| `_docker` | `(*args: str) -> str` | — | — |
| `proxy_url` | `()` | `@pytest.fixture()` | — |
| `_wait_until_serving` | `(url: str, timeout: float = 60.0) -> None` | — | — |
| `_forwarded_host` | `(url: str, path: str, host_header: str) -> str` | — | — |
| `test_proxy_forwards_mcp_host_with_port_and_guard_accepts_it` | `(proxy_url: str, mcp_path: str) -> None` | `@needs_docker`, `@pytest.mark.allow_network`, `@pytest.mark.parametrize('mcp_path', ['/api/mcp', '/api/mcp/'])` | — |
| `test_proxy_keeps_disallowed_host_visible_to_guard_as_421` | `(proxy_url: str) -> None` | `@needs_docker`, `@pytest.mark.allow_network` | — |
| `test_proxy_leaves_other_api_paths_on_bare_host` | `(proxy_url: str) -> None` | `@needs_docker`, `@pytest.mark.allow_network` | — |
