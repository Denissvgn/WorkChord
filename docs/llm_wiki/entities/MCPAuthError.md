# MCPAuthError

**Location:** `backend/app/mcp_server.py:43`
**Kind:** Class
**Bases:** `PermissionError`
**Module:** [mcp_server](../modules/mcp_server.md)

## Description

Raised when MCP agent authentication fails.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MCPAuthError (backend/app/mcp_server.py)"]
    n1["PermissionError"]
    n2["_agent_context (backend/app/mcp_server.py)"]
    n3["_authenticate_agent_key (backend/app/mcp_server.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/mcp_server.md"
    click n2 "../modules/mcp_server.md"
    click n3 "../modules/mcp_server.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [mcp_server](../modules/mcp_server.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `PermissionError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_agent_context` | call | [mcp_server](../modules/mcp_server.md) | 1 |
| `_authenticate_agent_key` | call | [mcp_server](../modules/mcp_server.md) | 3 |
