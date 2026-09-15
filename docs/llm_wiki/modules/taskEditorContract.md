# taskEditorContract Module

**Path:** `frontend/src/components/tasks/taskEditorContract.ts`

## Description

_Auto-generated from `frontend/src/components/tasks/taskEditorContract.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../types/task` | `Task`, `TaskCreate`, `TaskStatus`, `TaskUpdate` |
| `../../utils/apiError` | `getApiErrorMessage` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TASK_EDITOR_FIELD_SCHEMA`, `TaskConflictMetadata`, `TaskEditorAvailability`, `TaskEditorSection`, `TaskEditorServerError`, `TaskEditorValidationCode`, `TaskEditorValidationIssue`, `TaskEditorValues`, `buildTaskEditorDefaults`, `mapTaskEditorServerError`, `toTaskCreate`, `toTaskUpdate`, `validateTaskEditor` |
| Constants | `TASK_EDITOR_FIELD_SCHEMA` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/taskDraftStorage.ts"]
    n1["frontend/src/components/tasks/taskEditorContract.ts"]
    n2["frontend/src/components/tasks/TaskForm.tsx"]
    n3["frontend/src/types/task.ts"]
    n4["frontend/src/utils/apiError.ts"]
    n0 --> n1
    n1 --> n3
    n1 --> n4
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    click n0 "../modules/taskDraftStorage.md"
    click n1 "../modules/taskEditorContract.md"
    click n2 "../modules/TaskForm.md"
    click n3 "../modules/types_task.md"
    click n4 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [taskDraftStorage](../modules/taskDraftStorage.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [apiError](../modules/apiError.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskEditorValues](../entities/TaskEditorValues.md) | Class | 10 | — | — |
| [TaskEditorDefaultsContext](../entities/TaskEditorDefaultsContext.md) | Class | 33 | — | — |
| [TaskEditorFieldDefinition](../entities/TaskEditorFieldDefinition.md) | Class | 41 | — | — |
| [TaskEditorValidationIssue](../entities/TaskEditorValidationIssue.md) | Class | 185 | — | — |
| [TaskConflictMetadata](../entities/TaskConflictMetadata.md) | Class | 251 | — | — |
| [TaskEditorSection](../entities/TaskEditorSection.md) | Type alias | 4 | — | — |
| [TaskEditorAvailability](../entities/TaskEditorAvailability.md) | Type alias | 5 | — | — |
| [TaskEditorValidationCode](../entities/TaskEditorValidationCode.md) | Type alias | 178 | — | — |
| [TaskEditorServerError](../entities/TaskEditorServerError.md) | Type alias | 259 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `buildTaskEditorDefaults` | `(context: TaskEditorDefaultsContext = {}) -> TaskEditorValues` | — | — |
| `validateTaskEditor` | `(values: TaskEditorValues, iterationAssigneeIds: ReadonlySet<number>) -> TaskEditorValidationIssue[]` | — | — |
| `toTaskCreate` | `(values: TaskEditorValues) -> TaskCreate` | — | — |
| `toTaskUpdate` | `(values: TaskEditorValues, options: { includeStatus?: boolean } = {}) -> TaskUpdate` | — | — |
| `mapTaskEditorServerError` | `(error: unknown, fallback: string) -> TaskEditorServerError` | — | — |
