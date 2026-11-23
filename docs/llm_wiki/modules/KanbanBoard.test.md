# KanbanBoard.test Module

**Path:** `frontend/src/components/tasks/KanbanBoard/KanbanBoard.test.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/KanbanBoard/KanbanBoard.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../../components/common/Button` | `Button` | — | compiler-dependent |
| `../../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../../types/task` | `Task` | Declaration | erased |
| `../../../types/team` | `TeamMember` | Declaration | erased |
| `./KanbanBoard` | `KanbanBoard` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `dragState`, `taskServiceMock`, `teamServiceMock`, `planningMock`, `labelServiceMock` |
| Module calls | `dragState = hoisted`, `taskServiceMock = hoisted`, `teamServiceMock = hoisted`, `planningMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/tasks/KanbanBoard/KanbanBoard.test.tsx"]
    n2["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n4["frontend/src/types/task.ts"]
    n5["frontend/src/types/team.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n2 --> n0
    n2 --> n4
    n2 --> n5
    n4 --> n5
    click n0 "../modules/Button.md"
    click n1 "../modules/KanbanBoard.test.md"
    click n2 "../modules/KanbanBoard.md"
    click n3 "../modules/renderWithProviders.md"
    click n4 "../modules/types_task.md"
    click n5 "../modules/types_team.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [Button](../modules/Button.md) |
| Outbound | [KanbanBoard](../modules/KanbanBoard.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [types_team](../modules/types_team.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [DndContextMockProps](../entities/DndContextMockProps.md) | Interface | 37 | — | — |
