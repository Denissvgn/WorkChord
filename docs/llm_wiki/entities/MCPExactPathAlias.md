# MCPExactPathAlias

**Location:** `backend/app/mcp_server.py:151`
**Kind:** Class
**Bases:** —
**Module:** [mcp_server](../modules/mcp_server.md)

## Description

Route exact MCP mount path requests into the Streamable HTTP root app.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(app: ASGIApp, mount_path: str)` | — | — |
| `__call__` | *(async)* `(scope: Scope, receive: Receive, send: Send) -> None` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MCPExactPathAlias (backend/app/mcp_server.py)"]
    n1["mount_mcp_http (backend/app/mcp_server.py)"]
    n1 --> n0
    click n0 "../modules/mcp_server.md"
    click n1 "../modules/mcp_server.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [mcp_server](../modules/mcp_server.md) | 2 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mount_mcp_http` | call | [mcp_server](../modules/mcp_server.md) | 1 |
