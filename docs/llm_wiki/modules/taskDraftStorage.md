# taskDraftStorage Module

**Path:** `frontend/src/components/tasks/taskDraftStorage.ts`

## Description

Private task draft records can retain a pending operation marker alongside the original editor values. Recovery does not silently advance expected task versions or retry writes.

Private task draft values include the captured creation revision; malformed revisions are rejected on recovery. Pending-operation intent remains separately checkpointed.

## Imports

| Source | Symbols |
|--------|---------|
| `./taskEditorContract` | `TaskEditorValues` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PendingTaskWrite`, `readPendingTaskWrite`, `readTaskDraft`, `removeTaskDraft`, `writeTaskDraft` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/taskDraftStorage.test.ts"]
    n1["frontend/src/components/tasks/taskDraftStorage.ts"]
    n2["frontend/src/components/tasks/taskEditorContract.ts"]
    n3["frontend/src/components/tasks/TaskForm.tsx"]
    n4["frontend/src/pages/MyWorkPage.test.tsx"]
    n0 --> n1
    n1 --> n2
    n3 --> n1
    n3 --> n2
    n4 --> n1
    n4 --> n2
    click n0 "../modules/taskDraftStorage.test.md"
    click n1 "../modules/taskDraftStorage.md"
    click n2 "../modules/taskEditorContract.md"
    click n3 "../modules/TaskForm.md"
    click n4 "../modules/MyWorkPage.test.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [taskDraftStorage.test](../modules/taskDraftStorage.test.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [MyWorkPage.test](../modules/MyWorkPage.test.md) |
| Outbound | [taskEditorContract](../modules/taskEditorContract.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [PendingTaskWrite](../entities/PendingTaskWrite.md) | Type alias | 37 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `readTaskDraft` | `(key: string \| null, defaults: TaskEditorValues) -> TaskEditorValues \| null` | — | — |
| `readPendingTaskWrite` | `(key: string \| null) -> PendingTaskWrite \| null` | — | — |
| `writeTaskDraft` | `(key: string \| null, values: TaskEditorValues, pendingWrite: PendingTaskWrite \| null = null)` | — | — |
| `removeTaskDraft` | `(key: string \| null, includeProgress = false)` | — | — |