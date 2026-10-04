# MCPAgentKeyMiddleware

**Location:** `backend/app/mcp_server.py:105`
**Kind:** Class
**Bases:** —
**Module:** [mcp_server](../modules/mcp_server.md)

## Description

Extract and validate MCP HTTP agent credentials before protocol handling.

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
    n0["MCPAgentKeyMiddleware (backend/app/mcp_server.py)"]
    n1["create_mcp_http_app (backend/app/mcp_server.py)"]
    n2["test_mcp_http_uses_the_same_principal_and_project_boundary (backend/tests/test_identity_lifecycle.py)"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/mcp_server.md"
    click n1 "../modules/mcp_server.md"
    click n2 "../modules/test_identity_lifecycle.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [mcp_server](../modules/mcp_server.md) | 2 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_mcp_http_app` | call | [mcp_server](../modules/mcp_server.md) | 1 |
| `test_mcp_http_uses_the_same_principal_and_project_boundary` | call | [test_identity_lifecycle](../modules/test_identity_lifecycle.md) | 1 |
