# TaskFormProps

**Location:** `frontend/src/components/tasks/TaskForm.tsx:56`
**Kind:** Class
**Bases:** —
**Module:** [TaskForm](../modules/TaskForm.md)

## Description

_Auto-generated from `TaskFormProps` in `frontend/src/components/tasks/TaskForm.tsx`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `iterationId` | `number \| null` | Yes | — | — |
| `initialData` | `Task` | No | — | — |
| `parentId` | `number \| null` | No | — | — |
| `parentPriority` | `number` | No | — | — |
| `parentProjectId` | `number \| null` | No | — | — |
| `parentMilestoneId` | `number \| null` | No | — | — |
| `onSuccess` | `() => void` | Yes | — | — |
| `onCancel` | `() => void` | Yes | — | — |
| `mode` | `'direct' \| 'sandbox'` | No | — | — |
| `onSaveSandbox` | `(update: TaskUpdate) => void` | No | — | — |
| `onDirtyChange` | `(dirty: boolean) => void` | No | — | — |
| `onPendingChange` | `(pending: boolean) => void` | No | — | — |
| `onDiscardReady` | `(handler: (() => void) \| null) => void` | No | — | — |
| `confirmUnsavedOnCancel` | `boolean` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskFormProps (frontend/src/components/tasks/TaskForm.tsx)"]
    n1["TaskForm (frontend/src/components/tasks/TaskForm.tsx)"]
    n1 --> n0
    click n0 "../modules/TaskForm.md"
    click n1 "../modules/TaskForm.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TaskForm](../modules/TaskForm.md) | 0 | `confirmUnsavedOnCancel`, `initialData`, `iterationId`, `mode`, `onCancel`, `onDirtyChange`, `onDiscardReady`, `onPendingChange`, `onSaveSandbox`, `onSuccess`, `parentId`, `parentMilestoneId` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskForm` | type_reference | [TaskForm](../modules/TaskForm.md) | — |
