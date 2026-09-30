# KanbanCard Module

**Path:** `frontend/src/components/tasks/KanbanBoard/KanbanCard.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/KanbanBoard/KanbanCard.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../../i18n/i18n` | `i18n` |
| `../../../types/task` | `Task` |
| `@dnd-kit/sortable` | `useSortable` |
| `@dnd-kit/utilities` | `CSS` |
| `clsx` | `clsx` |
| `lucide-react` | `Bot`, `Clock`, `User`, `AlertCircle`, `GripVertical` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `KanbanCard` |
| Constants | `t` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n1["frontend/src/components/tasks/KanbanBoard/KanbanCard.tsx"]
    n2["frontend/src/components/tasks/KanbanBoard/KanbanColumn.tsx"]
    n3["frontend/src/i18n/i18n.ts"]
    n4["frontend/src/types/task.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n4
    n1 --> n3
    n1 --> n4
    n2 --> n1
    n2 --> n3
    n2 --> n4
    click n0 "../modules/KanbanBoard.md"
    click n1 "../modules/KanbanCard.md"
    click n2 "../modules/KanbanColumn.md"
    click n3 "../modules/i18n.md"
    click n4 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [KanbanBoard](../modules/KanbanBoard.md) |
| Inbound | [KanbanColumn](../modules/KanbanColumn.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [KanbanCardProps](../entities/KanbanCardProps.md) | Class | 10 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `KanbanCard` | `({ task, onOpen }: KanbanCardProps)` | — | — |
