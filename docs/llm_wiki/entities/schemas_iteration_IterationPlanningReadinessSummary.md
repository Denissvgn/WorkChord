# IterationPlanningReadinessSummary

**Location:** `backend/app/schemas/iteration.py:118`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_iteration](../modules/schemas_iteration.md)

## Description

Compact planning inputs used by persistent navigation.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `iteration_id` | `int` | `iteration_id` | Yes | No | — | — | — | — |
| `team_member_count` | `int` | `team_member_count` | Yes | No | — | — | — | — |
| `team_agent_count` | `int` | `team_agent_count` | No | No | `0` | — | — | — |
| `team_capacity_hours` | `float` | `team_capacity_hours` | Yes | No | — | — | — | — |
| `team_members_no_capacity` | `int` | `team_members_no_capacity` | Yes | No | — | — | — | — |
| `task_count` | `int` | `task_count` | Yes | No | — | — | — | — |
| `tasks_without_assignee` | `int` | `tasks_without_assignee` | Yes | No | — | — | — | — |
| `tasks_without_effort` | `int` | `tasks_without_effort` | Yes | No | — | — | — | — |
| `tasks_agent_without_capacity` | `int` | `tasks_agent_without_capacity` | No | No | `0` | — | — | — |
| `has_schedule` | `bool` | `has_schedule` | Yes | No | — | — | — | — |
| `risk_count` | `int` | `risk_count` | Yes | No | — | — | — | — |
| `checkpoints` | `list[PlanCheckpoint]` | `checkpoints` | No | No | factory: `list` | — | — | — |
| `checkpoints_done` | `int` | `checkpoints_done` | No | No | `0` | — | — | — |
| `checkpoints_total` | `int` | `checkpoints_total` | No | No | `6` | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["IterationPlanningReadinessSummary (backend/app/schemas/iteration.py)"]
    n1["BaseModel"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["get_iteration_plan_readiness (backend/app/routers/agent_planning.py)"]
    n4["get_iteration_planning_readiness (backend/app/routers/iterations.py)"]
    n5["IterationService.get_planning_readiness_summary (backend/app/services/iteration_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/schemas_iteration.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent_planning.md"
    click n4 "../modules/iterations.md"
    click n5 "../modules/iteration_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_iteration](../modules/schemas_iteration.md) | 0 | `checkpoints`, `checkpoints_done`, `checkpoints_total`, `has_schedule`, `iteration_id`, `risk_count`, `task_count`, `tasks_agent_without_capacity`, `tasks_without_assignee`, `tasks_without_effort`, `team_agent_count`, `team_capacity_hours` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `get_iteration_plan_readiness` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `get_iteration_planning_readiness` | type_reference | [iterations](../modules/iterations.md) | — |
| `IterationService.get_planning_readiness_summary` | call | [iteration_service](../modules/iteration_service.md) | 1 |
| `IterationService.get_planning_readiness_summary` | type_reference | [iteration_service](../modules/iteration_service.md) | — |
