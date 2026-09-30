# selectWorkNowTasks Module

**Path:** `frontend/src/utils/selectWorkNowTasks.ts`

## Description

_Auto-generated from `frontend/src/utils/selectWorkNowTasks.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/task` | `Task` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `selectWorkNowTasks` |
| Constants | `doneStatuses` |
| Module calls | `doneStatuses = Set` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/pages/OverviewPage.test.tsx"]
    n1["frontend/src/pages/OverviewPage.tsx"]
    n2["frontend/src/types/task.ts"]
    n3["frontend/src/utils/selectWorkNowTasks.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n2
    n1 --> n3
    n3 --> n2
    click n0 "../modules/OverviewPage.test.md"
    click n1 "../modules/OverviewPage.md"
    click n2 "../modules/types_task.md"
    click n3 "../modules/selectWorkNowTasks.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [OverviewPage.test](../modules/OverviewPage.test.md) |
| Inbound | [OverviewPage](../modules/OverviewPage.md) |
| Outbound | [types_task](../modules/types_task.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `selectWorkNowTasks` | `(tasks: Task[], limit = 3)` | — | — |
