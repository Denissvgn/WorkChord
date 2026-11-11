# KanbanColumn.test Module

**Path:** `frontend/src/components/tasks/KanbanBoard/KanbanColumn.test.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/KanbanBoard/KanbanColumn.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../../types/task` | `Task` | Declaration | erased |
| `./KanbanCard` | `KanbanCard` | — | compiler-dependent |
| `./KanbanColumn` | `KanbanColumn` | — | compiler-dependent |
| `./claimTime` | `formatClaimUntil` | — | compiler-dependent |
| `@testing-library/react` | `screen` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |
| `vitest` | `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `mock`, `mock`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/KanbanBoard/claimTime.ts"]
    n1["frontend/src/components/tasks/KanbanBoard/KanbanCard.tsx"]
    n2["frontend/src/components/tasks/KanbanBoard/KanbanColumn.test.tsx"]
    n3["frontend/src/components/tasks/KanbanBoard/KanbanColumn.tsx"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/types/task.ts"]
    n1 --> n0
    n1 --> n5
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n3 --> n1
    n3 --> n5
    click n0 "../modules/claimTime.md"
    click n1 "../modules/KanbanCard.md"
    click n2 "../modules/KanbanColumn.test.md"
    click n3 "../modules/KanbanColumn.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [claimTime](../modules/claimTime.md) |
| Outbound | [KanbanCard](../modules/KanbanCard.md) |
| Outbound | [KanbanColumn](../modules/KanbanColumn.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
