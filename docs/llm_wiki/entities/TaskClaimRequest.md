# TaskClaimRequest

**Location:** `backend/app/schemas/agent.py:247`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Request to claim or renew a task lease.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `lease_seconds` | `int` | `lease_seconds` | No | No | `3600` | ge=60; le=86400 | — | — |
| `trace_id` | `Optional[str]` | `trace_id` | No | Yes | `None` | max_length=255 | — | — |
| `span_id` | `Optional[str]` | `span_id` | No | Yes | `None` | max_length=255 | — | — |
| `correlation_id` | `Optional[str]` | `correlation_id` | No | Yes | `None` | max_length=255 | — | — |
| `claim_id` | `Optional[str]` | `claim_id` | No | Yes | `None` | max_length=64; min_length=16 | — | — |
| `claim_generation` | `Optional[int]` | `claim_generation` | No | Yes | `None` | ge=1 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskClaimRequest (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["claim_task (backend/app/mcp_agent_tools.py)"]
    n3["renew_task (backend/app/mcp_agent_tools.py)"]
    n4["claim_task (backend/app/routers/agent.py)"]
    n5["renew_task_claim (backend/app/routers/agent.py)"]
    n6["AgentService.claim_task (backend/app/services/agent_service.py)"]
    n7["AgentService.renew_claim (backend/app/services/agent_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/schemas_agent.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/mcp_agent_tools.md"
    click n4 "../modules/routers_agent.md"
    click n5 "../modules/routers_agent.md"
    click n6 "../modules/agent_service.md"
    click n7 "../modules/agent_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 0 | `claim_generation`, `claim_id`, `correlation_id`, `lease_seconds`, `span_id`, `trace_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `claim_task` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `renew_task` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `claim_task` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `renew_task_claim` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentService.claim_task` | type_reference | [agent_service](../modules/agent_service.md) | — |
| `AgentService.renew_claim` | type_reference | [agent_service](../modules/agent_service.md) | — |
