# taskDraftStorage Module

**Path:** `frontend/src/components/tasks/taskDraftStorage.ts`

## Description

_Auto-generated from `frontend/src/components/tasks/taskDraftStorage.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./taskEditorContract` | `TaskEditorValues` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `readTaskDraft`, `removeTaskDraft`, `writeTaskDraft` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/taskDraftStorage.ts"]
    n1["frontend/src/components/tasks/taskEditorContract.ts"]
    n2["frontend/src/components/tasks/TaskForm.tsx"]
    n0 --> n1
    n2 --> n0
    n2 --> n1
    click n0 "../modules/taskDraftStorage.md"
    click n1 "../modules/taskEditorContract.md"
    click n2 "../modules/TaskForm.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Outbound | [taskEditorContract](../modules/taskEditorContract.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `readTaskDraft` | `(key: string \| null, defaults: TaskEditorValues) -> TaskEditorValues \| null` | — | — |
| `writeTaskDraft` | `(key: string \| null, values: TaskEditorValues)` | — | — |
| `removeTaskDraft` | `(key: string \| null)` | — | — |
