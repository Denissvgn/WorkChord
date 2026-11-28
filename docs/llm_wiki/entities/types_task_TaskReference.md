# TaskReference

**Location:** `frontend/src/types/task.ts:538`
**Kind:** Interface
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskReference` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `acceptance_current` | `boolean` | No | — | — |
| `project_name` | `string \| null` | No | — | — |
| `iteration_name` | `string \| null` | No | — | — |
| `blocked_reason` | `string \| null` | No | — | — |
| `canceled_at` | `string \| null` | No | — | — |
| `reviewer_name` | `string \| null` | No | — | — |
| `id` | `number` | Yes | — | — |
| `title` | `string` | Yes | — | — |
| `version` | `number` | Yes | — | — |
| `status` | `TaskStatus` | Yes | — | — |
| `displayed_state` | `TaskDisplayedState` | No | — | — |
| `project_id` | `number \| null` | Yes | — | — |
| `iteration_id` | `number \| null` | Yes | — | — |
| `parent_id` | `number \| null` | Yes | — | — |
| `owner_profile_id` | `number \| null` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskReference (frontend/src/types/task.ts)"]
    n1["frontend/src/components/planning/PlanWorkSection.tsx"]
    n2["taskSearchResultCopy (frontend/src/components/tasks/taskSearchResults.ts)"]
    n3["loadProjectBacklog (frontend/src/features/overview/overviewBacklog.ts)"]
    n4["frontend/src/features/overview/overviewSignals.test.ts"]
    n5["backlogRoots (frontend/src/features/overview/overviewSignals.ts)"]
    n6["frontend/src/pages/MyWorkPage.tsx"]
    n7["frontend/src/pages/OverviewPage.test.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/PlanWorkSection.md"
    click n2 "../modules/taskSearchResults.md"
    click n3 "../modules/overviewBacklog.md"
    click n4 "../modules/overviewSignals.test.md"
    click n5 "../modules/overviewSignals.md"
    click n6 "../modules/MyWorkPage.md"
    click n7 "../modules/OverviewPage.test.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `acceptance_current`, `blocked_reason`, `canceled_at`, `displayed_state`, `id`, `iteration_id`, `iteration_name`, `owner_profile_id`, `parent_id`, `project_id`, `project_name`, `reviewer_name` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `PlanWorkSection` | import | [PlanWorkSection](../modules/PlanWorkSection.md) | — |
| `taskSearchResultCopy` | type_reference | [taskSearchResults](../modules/taskSearchResults.md) | — |
| `loadProjectBacklog` | type_reference | [overviewBacklog](../modules/overviewBacklog.md) | — |
| `overviewSignals.test` | import | [overviewSignals.test](../modules/overviewSignals.test.md) | — |
| `backlogRoots` | type_reference | [overviewSignals](../modules/overviewSignals.md) | — |
| `MyWorkPage` | import | [MyWorkPage](../modules/MyWorkPage.md) | — |
| `OverviewPage.test` | import | [OverviewPage.test](../modules/OverviewPage.test.md) | — |
