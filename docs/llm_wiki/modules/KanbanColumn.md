# KanbanColumn Module

**Path:** `frontend/src/components/tasks/KanbanBoard/KanbanColumn.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/KanbanBoard/KanbanColumn.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../../types/task` | `Task` | Declaration | erased |
| `../../ui/tone` | `PillTone` | Declaration | erased |
| `../../ui/tone` | `toneDotClassName` | — | compiler-dependent |
| `./KanbanCard` | `KanbanCard` | — | compiler-dependent |
| `@dnd-kit/core` | `useDroppable` | — | compiler-dependent |
| `@dnd-kit/sortable` | `SortableContext`, `verticalListSortingStrategy` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `react` | `useMemo` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `KanbanColumn` |
| Constants | `t` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

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
| [KanbanColumnProps](../entities/KanbanColumnProps.md) | Interface | 13 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `KanbanColumn` | `({ id, title, tasks, count, tone, onOpen }: KanbanColumnProps)` | — | — |
