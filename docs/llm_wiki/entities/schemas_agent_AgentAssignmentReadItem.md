# AgentAssignmentReadItem

**Location:** `backend/app/schemas/agent.py:759`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

An assignment as a person reads it: who holds which task, for what, and on which model.

Routing evidence, the assigner's free-text reason and reviewer details stay
with agent-key reads.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `id` | `int` | `id` | Yes | No | — | — | — | — |
| `task_id` | `int` | `task_id` | Yes | No | — | — | — | — |
| `actor_id` | `int` | `actor_id` | Yes | No | — | — | — | — |
| `actor` | `Optional[AgentAssignmentActorSummary]` | `actor` | No | Yes | `None` | — | — | — |
| `team_member_id` | `Optional[int]` | `team_member_id` | No | Yes | `None` | — | — | — |
| `purpose` | `str` | `purpose` | Yes | No | — | — | — | — |
| `queue_class` | `str` | `queue_class` | Yes | No | — | — | — | — |
| `state` | `str` | `state` | Yes | No | — | — | — | — |
| `queue_rank` | `int` | `queue_rank` | Yes | No | — | — | — | — |
| `not_before` | `Optional[datetime]` | `not_before` | No | Yes | `None` | — | — | — |
| `task_version` | `int` | `task_version` | Yes | No | — | — | — | — |
| `model_binding_id` | `Optional[int]` | `model_binding_id` | No | Yes | `None` | — | — | — |
| `model_binding_revision` | `Optional[int]` | `model_binding_revision` | No | Yes | `None` | — | — | — |
| `model_binding_status` | `Literal['not_selected', 'current', 'stale', 'unresolved']` | `model_binding_status` | No | No | `'not_selected'` | — | — | — |
| `model_binding_stale_reasons` | `list[str]` | `model_binding_stale_reasons` | No | No | factory: `list` | — | — | — |
| `model` | `Optional[AgentAssignmentModelSummary]` | `model` | No | Yes | `None` | — | — | — |
| `created_at` | `datetime` | `created_at` | Yes | No | — | — | — | — |
| `updated_at` | `datetime` | `updated_at` | Yes | No | — | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentAssignmentReadItem (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["list_agent_assignments (backend/app/routers/agent.py)"]
    n3["AgentWorkService.list_assignments_for_people (backend/app/services/agent_work_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_agent.md"
    click n2 "../modules/routers_agent.md"
    click n3 "../modules/agent_work_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 0 | `actor`, `actor_id`, `created_at`, `id`, `model`, `model_binding_id`, `model_binding_revision`, `model_binding_stale_reasons`, `model_binding_status`, `not_before`, `purpose`, `queue_class` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `list_agent_assignments` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentWorkService.list_assignments_for_people` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService.list_assignments_for_people` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
