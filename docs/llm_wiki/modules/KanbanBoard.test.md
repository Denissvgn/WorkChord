# KanbanBoard.test Module

**Path:** `frontend/src/components/tasks/KanbanBoard/KanbanBoard.test.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/KanbanBoard/KanbanBoard.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../../test/renderWithProviders` | `renderWithProviders` |
| `../../../types/task` | `Task` |
| `../../../types/team` | `TeamMember` |
| `./KanbanBoard` | `KanbanBoard` |
| `@testing-library/react` | `screen`, `waitFor` |
| `react` | `ReactNode` |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `dragState`, `taskServiceMock`, `teamServiceMock`, `labelServiceMock` |
| Module calls | `dragState = hoisted`, `taskServiceMock = hoisted`, `teamServiceMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/KanbanBoard/KanbanBoard.test.tsx"]
    n1["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/task.ts"]
    n4["frontend/src/types/team.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n1 --> n3
    n3 --> n4
    click n0 "../modules/KanbanBoard.test.md"
    click n1 "../modules/KanbanBoard.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/types_task.md"
    click n4 "../modules/types_team.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
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
| [DndContextMockProps](../entities/DndContextMockProps.md) | Class | 29 | — | — |
