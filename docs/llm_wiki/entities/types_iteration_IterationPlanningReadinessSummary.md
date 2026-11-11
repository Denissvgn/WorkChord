# IterationPlanningReadinessSummary

**Location:** `frontend/src/types/iteration.ts:74`
**Kind:** Interface
**Bases:** —
**Module:** [types_iteration](../modules/types_iteration.md)

## Description

_Auto-generated from `IterationPlanningReadinessSummary` in `frontend/src/types/iteration.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `iteration_id` | `number` | Yes | — | — |
| `team_member_count` | `number` | Yes | — | — |
| `team_capacity_hours` | `number` | Yes | — | — |
| `team_members_no_capacity` | `number` | Yes | — | — |
| `task_count` | `number` | Yes | — | — |
| `tasks_without_assignee` | `number` | Yes | — | — |
| `tasks_without_effort` | `number` | Yes | — | — |
| `tasks_agent_without_capacity` | `number` | No | — | — |
| `team_agent_count` | `number` | No | — | — |
| `has_schedule` | `boolean` | Yes | — | — |
| `risk_count` | `number` | Yes | — | — |
| `checkpoints` | `PlanCheckpoint[]` | No | — | — |
| `checkpoints_done` | `number` | No | — | — |
| `checkpoints_total` | `number` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["IterationPlanningReadinessSummary (frontend/src/types/iteration.ts)"]
    n1["frontend/src/services/iterationService.ts"]
    n1 --> n0
    click n0 "../modules/types_iteration.md"
    click n1 "../modules/iterationService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_iteration](../modules/types_iteration.md) | 0 | `checkpoints`, `checkpoints_done`, `checkpoints_total`, `has_schedule`, `iteration_id`, `risk_count`, `task_count`, `tasks_agent_without_capacity`, `tasks_without_assignee`, `tasks_without_effort`, `team_agent_count`, `team_capacity_hours` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `iterationService` | import | [iterationService](../modules/iterationService.md) | — |
