# TaskEditDrawerProps

**Location:** `frontend/src/components/gantt/TaskEditDrawer.tsx:8`
**Kind:** Interface
**Bases:** —
**Module:** [TaskEditDrawer](../modules/TaskEditDrawer.md)

## Description

_Auto-generated from `TaskEditDrawerProps` in `frontend/src/components/gantt/TaskEditDrawer.tsx`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `task` | `GanttTask \| null` | Yes | — | — |
| `iterationId` | `number` | Yes | — | — |
| `isOpen` | `boolean` | Yes | — | — |
| `onClose` | `() => void` | Yes | — | — |
| `sandboxMode` | `boolean` | No | — | — |
| `onSaveSandbox` | `(taskId: number, updatedData: Partial<GanttTask>) => void` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskEditDrawerProps (frontend/src/components/gantt/TaskEditDrawer.tsx)"]
    n1["TaskEditDrawer (frontend/src/components/gantt/TaskEditDrawer.tsx)"]
    n1 --> n0
    click n0 "../modules/TaskEditDrawer.md"
    click n1 "../modules/TaskEditDrawer.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TaskEditDrawer](../modules/TaskEditDrawer.md) | 0 | `isOpen`, `iterationId`, `onClose`, `onSaveSandbox`, `sandboxMode`, `task` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskEditDrawer` | type_reference | [TaskEditDrawer](../modules/TaskEditDrawer.md) | — |
