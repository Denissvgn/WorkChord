# RowContext

**Location:** `frontend/src/components/tasks/TaskList.tsx:609`
**Kind:** Interface
**Bases:** —
**Module:** [TaskList](../modules/TaskList.md)

## Description

What every row of the list shares: selection, hierarchy state and inline edits.

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `onOpen` | `(task: Task) => void` | Yes | — | — |
| `onOpenSuccessor` | `(taskId: number) => void` | Yes | — | — |
| `onAddSubtask` | `(id: number) => void` | Yes | — | — |
| `onDelete` | `(task: Task) => void` | Yes | — | — |
| `onUnmerge` | `(taskId: number) => void` | Yes | — | — |
| `isUnmergePending` | `boolean` | Yes | — | — |
| `sensors` | `ReturnType<typeof useSensors>` | Yes | — | — |
| `onChildDragEnd` | `(parent: Task, event: DragEndEvent) => void` | Yes | — | — |
| `isDraggingEnabled` | `boolean` | Yes | — | — |
| `taskMap` | `Map<number, Task>` | Yes | — | — |
| `labelsBySlug` | `Map<string, Label>` | Yes | — | — |
| `nowMs` | `number` | Yes | — | — |
| `selectedIds` | `Set<number>` | Yes | — | — |
| `selectableIds` | `Set<number>` | Yes | — | — |
| `onToggleSelect` | `(taskId: number, shiftKey: boolean) => void` | Yes | — | — |
| `collapsedParents` | `Set<number>` | Yes | — | — |
| `onToggleParent` | `(taskId: number) => void` | Yes | — | — |
| `assigneeOptions` | `TaskRowAssigneeOption[]` | Yes | — | — |
| `agentFacts` | `AgentRowFacts` | Yes | — | — |
| `onAssign` | `(task: Task, assigneeId: number \| null) => void` | Yes | — | — |
| `onStatusChange` | `(task: Task, status: TaskStatus) => void` | Yes | — | — |
| `showRiskReasons` | `boolean` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TaskList](../modules/TaskList.md) | 0 | `agentFacts`, `assigneeOptions`, `collapsedParents`, `isDraggingEnabled`, `isUnmergePending`, `labelsBySlug`, `nowMs`, `onAddSubtask`, `onAssign`, `onChildDragEnd`, `onDelete`, `onOpen` |
