# MCPHostValidationMiddleware

**Location:** `backend/app/mcp_server.py:76`
**Kind:** Class
**Bases:** —
**Module:** [mcp_server](../modules/mcp_server.md)

## Description

Reject untrusted MCP Host/Origin values before database authentication.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(app: ASGIApp)` | — | — |
| `__call__` | *(async)* `(scope: Scope, receive: Receive, send: Send) -> None` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MCPHostValidationMiddleware (backend/app/mcp_server.py)"]
    n1["create_mcp_http_app (backend/app/mcp_server.py)"]
    n2["_guard_status (backend/tests/test_mcp_proxy_host_header.py)"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/mcp_server.md"
    click n1 "../modules/mcp_server.md"
    click n2 "../modules/test_mcp_proxy_host_header.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [mcp_server](../modules/mcp_server.md) | 2 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_mcp_http_app` | call | [mcp_server](../modules/mcp_server.md) | 1 |
| `_guard_status` | call | [test_mcp_proxy_host_header](../modules/test_mcp_proxy_host_header.md) | 1 |
