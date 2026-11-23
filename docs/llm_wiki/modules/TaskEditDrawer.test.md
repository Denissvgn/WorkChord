# TaskEditDrawer.test Module

**Path:** `frontend/src/components/gantt/TaskEditDrawer.test.tsx`

## Description

_Auto-generated from `frontend/src/components/gantt/TaskEditDrawer.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Button` | `Button` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/gantt` | `GanttTask` | Declaration | erased |
| `../../types/task` | `TaskDetail`, `TaskUpdate` | Declaration | erased |
| `./TaskEditDrawer` | `TaskEditDrawer` | — | compiler-dependent |
| `@testing-library/react` | `act`, `fireEvent`, `screen` | — | compiler-dependent |
| `vitest` | `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `api`, `ganttTask` |
| Module calls | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `it`, `it` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/gantt/TaskEditDrawer.test.tsx"]
    n2["frontend/src/components/gantt/TaskEditDrawer.tsx"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n4["frontend/src/types/gantt.ts"]
    n5["frontend/src/types/task.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n2 --> n4
    n2 --> n5
    n4 --> n5
    click n0 "../modules/Button.md"
    click n1 "../modules/TaskEditDrawer.test.md"
    click n2 "../modules/TaskEditDrawer.md"
    click n3 "../modules/renderWithProviders.md"
    click n4 "../modules/types_gantt.md"
    click n5 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [Button](../modules/Button.md) |
| Outbound | [TaskEditDrawer](../modules/TaskEditDrawer.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_gantt](../modules/types_gantt.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
