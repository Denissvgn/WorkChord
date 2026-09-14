# AgentPlanningReceipt

**Location:** `backend/app/schemas/agent_planning.py:31`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent_planning](../modules/schemas_agent_planning.md)

## Description

Exact durable response stored for one PM setup mutation.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `operation` | `str` | `operation` | Yes | No | — | — | — | — |
| `actor_id` | `int` | `actor_id` | Yes | No | — | — | — | — |
| `target_type` | `str` | `target_type` | Yes | No | — | — | — | — |
| `target_id` | `int` | `target_id` | Yes | No | — | — | — | — |
| `idempotency_key` | `str` | `idempotency_key` | Yes | No | — | — | — | — |
| `rationale` | `str` | `rationale` | Yes | No | — | — | — | — |
| `correlation_id` | `str` | `correlation_id` | Yes | No | — | — | — | — |
| `result` | `dict[str, Any]` | `result` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentPlanningReceipt (backend/app/schemas/agent_planning.py)"]
    n1["BaseModel"]
    n2["apply_schedule (backend/app/routers/agent_planning.py)"]
    n3["create_iteration (backend/app/routers/agent_planning.py)"]
    n4["create_planning_task (backend/app/routers/agent_planning.py)"]
    n5["create_profile (backend/app/routers/agent_planning.py)"]
    n6["create_project (backend/app/routers/agent_planning.py)"]
    n7["create_project_milestone (backend/app/routers/agent_planning.py)"]
    n8["create_team_member (backend/app/routers/agent_planning.py)"]
    n9["create_vacation (backend/app/routers/agent_planning.py)"]
    n10["delete_project_milestone (backend/app/routers/agent_planning.py)"]
    n11["patch_planning_task (backend/app/routers/agent_planning.py)"]
    n12["preview_schedule (backend/app/routers/agent_planning.py)"]
    n13["update_iteration (backend/app/routers/agent_planning.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    n13 --> n0
    click n0 "../modules/schemas_agent_planning.md"
    click n2 "../modules/routers_agent_planning.md"
    click n3 "../modules/routers_agent_planning.md"
    click n4 "../modules/routers_agent_planning.md"
    click n5 "../modules/routers_agent_planning.md"
    click n6 "../modules/routers_agent_planning.md"
    click n7 "../modules/routers_agent_planning.md"
    click n8 "../modules/routers_agent_planning.md"
    click n9 "../modules/routers_agent_planning.md"
    click n10 "../modules/routers_agent_planning.md"
    click n11 "../modules/routers_agent_planning.md"
    click n12 "../modules/routers_agent_planning.md"
    click n13 "../modules/routers_agent_planning.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent_planning](../modules/schemas_agent_planning.md) | 0 | `actor_id`, `correlation_id`, `idempotency_key`, `operation`, `rationale`, `result`, `target_id`, `target_type` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `apply_schedule` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `create_iteration` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `create_planning_task` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `create_profile` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `create_project` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `create_project_milestone` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `create_team_member` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `create_vacation` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `delete_project_milestone` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `patch_planning_task` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `preview_schedule` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `update_iteration` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |

> References: showing 12 of 38 logical references; 26 omitted by the 12-row generated summary limit.
