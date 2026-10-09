# CurrentTaskModal.test Module

**Path:** `frontend/src/components/tasks/CurrentTaskModal.test.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/CurrentTaskModal.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../test/renderWithProviders` | `renderWithProviders` |
| `../../types/task` | `Task`, `TaskDetail` |
| `./GuardedTaskModal` | `CurrentTaskModal` |
| `@testing-library/react` | `act`, `screen`, `waitFor` |
| `react` | `useEffect`, `useState` |
| `vitest` | `beforeEach`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `service` |
| Module calls | `service = hoisted`, `mock`, `mock`, `beforeEach`, `it`, `it`, `it`, `it`, `it` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/CurrentTaskModal.test.tsx"]
    n1["frontend/src/components/tasks/GuardedTaskModal.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/task.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n3
    click n0 "../modules/CurrentTaskModal.test.md"
    click n1 "../modules/GuardedTaskModal.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [GuardedTaskModal](../modules/GuardedTaskModal.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
