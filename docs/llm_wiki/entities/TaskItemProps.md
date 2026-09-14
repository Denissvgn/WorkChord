# TaskItemProps

**Location:** `frontend/src/components/tasks/TaskList.tsx:745`
**Kind:** Class
**Bases:** —
**Module:** [TaskList](../modules/TaskList.md)

## Description

_Auto-generated from `TaskItemProps` in `frontend/src/components/tasks/TaskList.tsx`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `task` | `Task` | *required* | — |
| `onEdit` | `(t: Task) => void` | *required* | — |
| `onAddSubtask` | `(id: number) => void` | *required* | — |
| `onDelete` | `(task: Task) => void` | *required* | — |
| `onUnmerge` | `(taskId: number) => void` | *required* | — |
| `isUnmergePending` | `boolean` | *required* | — |
| `level` | `number` | *required* | — |
| `sensors` | `ReturnType<typeof useSensors>` | *required* | — |
| `onChildDragEnd` | `(parent: Task, event: DragEndEvent) => void` | *required* | — |
| `isDraggingEnabled` | `boolean` | *required* | — |
| `taskMap` | `Map<number, Task>` | *required* | — |
| `isMergeMode` | `boolean` | *required* | — |
| `selectedTaskIds` | `Set<number>` | *required* | — |
| `canSelectForMerge` | `(task: Task) => boolean` | *required* | — |
| `toggleTaskSelection` | `(taskId: number) => void` | *required* | — |
| `isBulkMode` | `boolean` | *required* | — |
| `selectedBulkTaskIds` | `Set<number>` | *required* | — |
| `toggleBulkTaskSelection` | `(taskId: number) => void` | *required* | — |
| `labelsBySlug` | `Map<string, Label>` | *required* | — |
| `nowMs` | `number` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskItemProps (frontend/src/components/tasks/TaskList.tsx)"]
    n1["TaskItemContentProps (frontend/src/components/tasks/TaskList.tsx)"]
    n1 --> n0
    click n0 "../modules/TaskList.md"
    click n1 "../modules/TaskList.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TaskList](../modules/TaskList.md) | 0 | `canSelectForMerge`, `isBulkMode`, `isDraggingEnabled`, `isMergeMode`, `isUnmergePending`, `labelsBySlug`, `level`, `nowMs`, `onAddSubtask`, `onChildDragEnd`, `onDelete`, `onEdit` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Subclass | `TaskItemContentProps` | [TaskList](../modules/TaskList.md) |
