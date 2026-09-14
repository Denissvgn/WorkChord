# RequestSourceLinkWithSourceResponse

**Location:** `backend/app/schemas/request_source.py:148`
**Kind:** Pydantic model
**Bases:** `RequestSourceLinkResponse`
**Module:** [schemas_request_source](../modules/schemas_request_source.md)

## Description

Request-source link response with embedded source details.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `request_source` | `RequestSourceResponse` | `request_source` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RequestSourceLinkWithSourceResponse (backend/app/schemas/request_source.py)"]
    n1["RequestSourceLinkResponse (backend/app/schemas/request_source.py)"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["create_request_source_link (backend/app/routers/request_sources.py)"]
    n4["list_request_source_links (backend/app/routers/request_sources.py)"]
    n5["backend/app/schemas/__init__.py"]
    n6["backend/app/schemas/agent.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/schemas_request_source.md"
    click n1 "../modules/schemas_request_source.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/request_sources.md"
    click n4 "../modules/request_sources.md"
    click n5 "../modules/schemas___init__.md"
    click n6 "../modules/schemas_agent.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_request_source](../modules/schemas_request_source.md) | 0 | `request_source` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RequestSourceLinkResponse` | [schemas_request_source](../modules/schemas_request_source.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `create_request_source_link` | type_reference | [request_sources](../modules/request_sources.md) | — |
| `list_request_source_links` | type_reference | [request_sources](../modules/request_sources.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `agent` | import | [schemas_agent](../modules/schemas_agent.md) | — |
