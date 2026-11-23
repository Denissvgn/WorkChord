# KanbanColumnProps

**Location:** `frontend/src/components/tasks/KanbanBoard/KanbanColumn.tsx:16`
**Kind:** Interface
**Bases:** —
**Module:** [KanbanColumn](../modules/KanbanColumn.md)

## Description

_Auto-generated from `KanbanColumnProps` in `frontend/src/components/tasks/KanbanBoard/KanbanColumn.tsx`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `string` | Yes | — | — |
| `title` | `string` | Yes | — | — |
| `tasks` | `Task[]` | Yes | — | — |
| `count` | `number` | Yes | — | — |
| `caption` | `string` | No | — | — |
| `tone` | `PillTone` | Yes | — | — |
| `onOpen` | `(task: Task, trigger?: HTMLElement) => void` | No | — | — |
| `context` | `BoardCardContext` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["KanbanColumnProps (frontend/src/components/tasks/KanbanBoard/KanbanColumn.tsx)"]
    n1["KanbanColumn (frontend/src/components/tasks/KanbanBoard/KanbanColumn.tsx)"]
    n1 --> n0
    click n0 "../modules/KanbanColumn.md"
    click n1 "../modules/KanbanColumn.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [KanbanColumn](../modules/KanbanColumn.md) | 0 | `caption`, `context`, `count`, `id`, `onOpen`, `tasks`, `title`, `tone` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `KanbanColumn` | type_reference | [KanbanColumn](../modules/KanbanColumn.md) | — |
