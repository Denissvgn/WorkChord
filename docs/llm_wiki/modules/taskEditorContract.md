# taskEditorContract Module

**Path:** `frontend/src/components/tasks/taskEditorContract.ts`

## Description

_Auto-generated from `frontend/src/components/tasks/taskEditorContract.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../types/task` | `Task`, `TaskBrief`, `TaskCreate`, `TaskStatus`, `TaskUpdate` |
| `../../utils/apiError` | `getApiErrorMessage` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TASK_EDITOR_FIELD_SCHEMA`, `TaskConflictMetadata`, `TaskEditorAvailability`, `TaskEditorSection`, `TaskEditorServerError`, `TaskEditorValidationCode`, `TaskEditorValidationIssue`, `TaskEditorValues`, `buildTaskEditorDefaults`, `emptyTaskBrief`, `mapTaskEditorServerError`, `newCriterion`, `toTaskCreate`, `toTaskUpdate`, `validateTaskEditor` |
| Constants | `TASK_EDITOR_FIELD_SCHEMA` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskBriefEditor.test.tsx"]
    n1["frontend/src/components/tasks/TaskBriefEditor.tsx"]
    n2["frontend/src/components/tasks/taskDraftStorage.ts"]
    n3["frontend/src/components/tasks/taskEditorContract.ts"]
    n4["frontend/src/components/tasks/TaskForm.test.tsx"]
    n5["frontend/src/components/tasks/TaskForm.tsx"]
    n6["frontend/src/components/tasks/TaskWorkPanel.test.tsx"]
    n7["frontend/src/pages/MyWorkPage.test.tsx"]
    n8["frontend/src/pages/TriagePage.tsx"]
    n9["frontend/src/types/task.ts"]
    n10["frontend/src/utils/apiError.ts"]
    n0 --> n1
    n0 --> n3
    n1 --> n3
    n1 --> n9
    n2 --> n3
    n3 --> n9
    n3 --> n10
    n4 --> n3
    n4 --> n5
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n9
    n5 --> n10
    n6 --> n3
    n6 --> n9
    n7 --> n2
    n7 --> n3
    n7 --> n9
    n8 --> n1
    n8 --> n3
    n8 --> n9
    n8 --> n10
    click n0 "../modules/TaskBriefEditor.test.md"
    click n1 "../modules/TaskBriefEditor.md"
    click n2 "../modules/taskDraftStorage.md"
    click n3 "../modules/taskEditorContract.md"
    click n4 "../modules/TaskForm.test.md"
    click n5 "../modules/TaskForm.md"
    click n6 "../modules/TaskWorkPanel.test.md"
    click n7 "../modules/MyWorkPage.test.md"
    click n8 "../modules/TriagePage.md"
    click n9 "../modules/types_task.md"
    click n10 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskBriefEditor.test](../modules/TaskBriefEditor.test.md) |
| Inbound | [TaskBriefEditor](../modules/TaskBriefEditor.md) |
| Inbound | [taskDraftStorage](../modules/taskDraftStorage.md) |
| Inbound | [TaskForm.test](../modules/TaskForm.test.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TaskWorkPanel.test](../modules/TaskWorkPanel.test.md) |
| Inbound | [MyWorkPage.test](../modules/MyWorkPage.test.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [apiError](../modules/apiError.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskEditorValues](../entities/TaskEditorValues.md) | Class | 10 | — | — |
| [TaskEditorDefaultsContext](../entities/TaskEditorDefaultsContext.md) | Class | 37 | — | — |
| [TaskEditorFieldDefinition](../entities/TaskEditorFieldDefinition.md) | Class | 45 | — | — |
| [TaskEditorValidationIssue](../entities/TaskEditorValidationIssue.md) | Class | 196 | — | — |
| [TaskConflictMetadata](../entities/TaskConflictMetadata.md) | Class | 265 | — | — |
| [TaskEditorSection](../entities/TaskEditorSection.md) | Type alias | 4 | — | — |
| [TaskEditorAvailability](../entities/TaskEditorAvailability.md) | Type alias | 5 | — | — |
| [TaskEditorValidationCode](../entities/TaskEditorValidationCode.md) | Type alias | 189 | — | — |
| [TaskEditorServerError](../entities/TaskEditorServerError.md) | Type alias | 273 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `emptyTaskBrief` | `() -> TaskBrief` | — | — |
| `buildTaskEditorDefaults` | `(context: TaskEditorDefaultsContext = {}) -> TaskEditorValues` | — | — |
| `validateTaskEditor` | `(values: TaskEditorValues, iterationAssigneeIds: ReadonlySet<number>) -> TaskEditorValidationIssue[]` | — | — |
| `toTaskCreate` | `(values: TaskEditorValues) -> TaskCreate` | — | — |
| `toTaskUpdate` | `(values: TaskEditorValues, options: { includeStatus?: boolean } = {}) -> TaskUpdate` | — | — |
| `mapTaskEditorServerError` | `(error: unknown, fallback: string) -> TaskEditorServerError` | — | — |
| `newCriterion` | `(text = '')` | — | — |
