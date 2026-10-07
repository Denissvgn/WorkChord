# AgentRunDetailResponse

**Location:** `backend/app/schemas/agent.py:487`
**Kind:** Pydantic model
**Bases:** `AgentRunResponse`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Full detail of an agent run including its list of chronological trace events.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `events` | `list[AgentRunEventResponse]` | `events` | No | No | `[]` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentRunDetailResponse (backend/app/schemas/agent.py)"]
    n1["AgentRunResponse (backend/app/schemas/agent.py)"]
    n2["get_agent_run_detail (backend/app/mcp_agent_tools.py)"]
    n3["_run_detail_response (backend/app/routers/agent.py)"]
    n4["get_agent_run_detail (backend/app/routers/agent.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_agent.md"
    click n1 "../modules/schemas_agent.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent.md"
    click n4 "../modules/routers_agent.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 0 | `events` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `AgentRunResponse` | [schemas_agent](../modules/schemas_agent.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_agent_run_detail` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `_run_detail_response` | call | [routers_agent](../modules/routers_agent.md) | 1 |
| `_run_detail_response` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `get_agent_run_detail` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
