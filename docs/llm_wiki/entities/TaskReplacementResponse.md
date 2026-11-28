# TaskReplacementResponse

**Location:** `backend/app/schemas/task_replacement.py:129`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task_replacement](../modules/schemas_task_replacement.md)

## Description

A recorded replacement or supersession as seen from one of its tasks, with its role (original, replacement or successor), the decision, the review policy, both tasks, carried contributions, what moved, and the acceptance state. Acceptance is `clean` or `held`, and a hold names why, such as carried work with no attribution.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `id` | `int` | `id` | Yes | No | — | — | — | — |
| `project_id` | `int` | `project_id` | Yes | No | — | — | — | — |
| `disposition` | `Literal['replacement', 'supersession']` | `disposition` | Yes | No | — | — | — | — |
| `role` | `Literal['original', 'replacement', 'successor']` | `role` | Yes | No | — | — | — | — |
| `original_task_id` | `int` | `original_task_id` | Yes | No | — | — | — | — |
| `replacement_task_id` | `int` | `replacement_task_id` | Yes | No | — | — | — | — |
| `decision` | `ReplacementDecision` | `decision` | Yes | No | — | — | — | — |
| `review_policy` | `ReplacementReviewPolicy` | `review_policy` | Yes | No | — | — | — | — |
| `original` | `ReplacementOriginal` | `original` | Yes | No | — | — | — | — |
| `replacement` | `ReplacementTask` | `replacement` | Yes | No | — | — | — | — |
| `carried_contributions` | `list[ReplacementContributor]` | `carried_contributions` | Yes | No | — | — | — | — |
| `moved_dependencies` | `list[ReplacementMovedDependency]` | `moved_dependencies` | Yes | No | — | — | — | — |
| `moved_release_ids` | `list[int]` | `moved_release_ids` | Yes | No | — | — | — | — |
| `acceptance` | `ReplacementAcceptance` | `acceptance` | Yes | No | — | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskReplacementResponse (backend/app/schemas/task_replacement.py)"]
    n1["BaseModel"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["get_task_replacement (backend/app/routers/agent_planning.py)"]
    n4["record_task_replacement (backend/app/routers/task_domain.py)"]
    n5["record_task_supersession (backend/app/routers/task_domain.py)"]
    n6["task_replacement (backend/app/routers/task_domain.py)"]
    n7["backend/app/services/agent_planning_service.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/schemas_task_replacement.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent_planning.md"
    click n4 "../modules/routers_task_domain.md"
    click n5 "../modules/routers_task_domain.md"
    click n6 "../modules/routers_task_domain.md"
    click n7 "../modules/agent_planning_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task_replacement](../modules/schemas_task_replacement.md) | 0 | `acceptance`, `carried_contributions`, `decision`, `disposition`, `id`, `moved_dependencies`, `moved_release_ids`, `original`, `original_task_id`, `project_id`, `replacement`, `replacement_task_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `get_task_replacement` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `record_task_replacement` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `record_task_supersession` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `task_replacement` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `agent_planning_service` | import | [agent_planning_service](../modules/agent_planning_service.md) | — |
