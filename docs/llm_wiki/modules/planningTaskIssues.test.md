# planningTaskIssues.test Module

**Path:** `frontend/src/features/planningMasters/planningTaskIssues.test.ts`

## Description

_Auto-generated from `frontend/src/features/planningMasters/planningTaskIssues.test.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/task` | `Task` | Declaration | erased |
| `./planningTaskIssues` | `hasPositivePlanningEffort`, `isPlanningLeafTask`, `parsePlanningIterationId`, `parsePlanningTaskIssue`, `planningIssueTasksHref`, `taskMatchesPlanningIssue` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/features/planningMasters/planningTaskIssues.test.ts"]
    n1["frontend/src/features/planningMasters/planningTaskIssues.ts"]
    n2["frontend/src/types/task.ts"]
    n0 --> n1
    n0 --> n2
    n1 --> n2
    click n0 "../modules/planningTaskIssues.test.md"
    click n1 "../modules/planningTaskIssues.md"
    click n2 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [planningTaskIssues](../modules/planningTaskIssues.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |
