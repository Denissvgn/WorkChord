# TaskBulkOperationRequest

**Location:** `frontend/src/types/task.ts:341`
**Kind:** Interface
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskBulkOperationRequest` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `expected_versions` | `Record<number, number>` | No | — | — |
| `expected_revisions` | `Record<number, number>` | No | — | — |
| `task_ids` | `number[]` | Yes | — | — |
| `action` | `TaskBulkAction` | Yes | — | — |
| `payload` | `Record<string, unknown>` | No | — | — |
| `dry_run` | `boolean` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskBulkOperationRequest (frontend/src/types/task.ts)"]
    n1["frontend/src/components/planning/PlanBlockersSection.tsx"]
    n2["frontend/src/pages/PlanPage.test.tsx"]
    n3["frontend/src/services/taskService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/PlanBlockersSection.md"
    click n2 "../modules/PlanPage.test.md"
    click n3 "../modules/taskService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `action`, `dry_run`, `expected_revisions`, `expected_versions`, `payload`, `task_ids` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `PlanBlockersSection` | import | [PlanBlockersSection](../modules/PlanBlockersSection.md) | — |
| `PlanPage.test` | import | [PlanPage.test](../modules/PlanPage.test.md) | — |
| `taskService` | import | [taskService](../modules/taskService.md) | — |
