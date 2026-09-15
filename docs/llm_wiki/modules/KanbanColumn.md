# KanbanColumn Module

**Path:** `frontend/src/components/tasks/KanbanBoard/KanbanColumn.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/KanbanBoard/KanbanColumn.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../../i18n/i18n` | `i18n` |
| `../../../types/task` | `Task` |
| `../../ui/tone` | `PillTone`, `toneDotClassName` |
| `./KanbanCard` | `KanbanCard` |
| `@dnd-kit/core` | `useDroppable` |
| `@dnd-kit/sortable` | `SortableContext`, `verticalListSortingStrategy` |
| `clsx` | `clsx` |
| `react` | `useMemo` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `KanbanColumn` |
| Constants | `t` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n1["frontend/src/components/tasks/KanbanBoard/KanbanCard.tsx"]
    n2["frontend/src/components/tasks/KanbanBoard/KanbanColumn.tsx"]
    n3["frontend/src/components/ui/tone.ts"]
    n4["frontend/src/i18n/i18n.ts"]
    n5["frontend/src/types/task.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n5
    n1 --> n4
    n1 --> n5
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n3 --> n5
    click n0 "../modules/KanbanBoard.md"
    click n1 "../modules/KanbanCard.md"
    click n2 "../modules/KanbanColumn.md"
    click n3 "../modules/tone.md"
    click n4 "../modules/i18n.md"
    click n5 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [KanbanBoard](../modules/KanbanBoard.md) |
| Outbound | [KanbanCard](../modules/KanbanCard.md) |
| Outbound | [tone](../modules/tone.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [KanbanColumnProps](../entities/KanbanColumnProps.md) | Class | 13 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `KanbanColumn` | `({ id, title, tasks, count, tone, onOpen }: KanbanColumnProps)` | — | — |
