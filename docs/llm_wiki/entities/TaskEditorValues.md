# TaskEditorValues

**Location:** `frontend/src/components/tasks/taskEditorContract.ts:10`
**Kind:** Class
**Bases:** —
**Module:** [taskEditorContract](../modules/taskEditorContract.md)

## Description

_Auto-generated from `TaskEditorValues` in `frontend/src/components/tasks/taskEditorContract.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `string` | *required* | — |
| `description` | `string` | *required* | — |
| `priority` | `number` | *required* | — |
| `effort_days` | `number` | *required* | — |
| `effort_hours` | `number` | *required* | — |
| `assignee_id` | `number \| null` | *required* | — |
| `project_id` | `number \| null` | *required* | — |
| `milestone_id` | `number \| null` | *required* | — |
| `parent_id` | `number \| null` | *required* | — |
| `depends_on` | `number[]` | *required* | — |
| `is_optional` | `boolean` | *required* | — |
| `is_deferred` | `boolean` | *required* | — |
| `tags` | `string[]` | *required* | — |
| `min_start_date` | `string \| null` | *required* | — |
| `max_end_date` | `string \| null` | *required* | — |
| `external_key` | `string \| null` | *required* | — |
| `source` | `string \| null` | *required* | — |
| `source_url` | `string \| null` | *required* | — |
| `status` | `TaskStatus` | *required* | — |
| `expected_version` | `number \| null` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskEditorValues (frontend/src/components/tasks/taskEditorContract.ts)"]
    n1["readTaskDraft (frontend/src/components/tasks/taskDraftStorage.ts)"]
    n2["writeTaskDraft (frontend/src/components/tasks/taskDraftStorage.ts)"]
    n3["buildTaskEditorDefaults (frontend/src/components/tasks/taskEditorContract.ts)"]
    n4["toTaskCreate (frontend/src/components/tasks/taskEditorContract.ts)"]
    n5["toTaskUpdate (frontend/src/components/tasks/taskEditorContract.ts)"]
    n6["validateTaskEditor (frontend/src/components/tasks/taskEditorContract.ts)"]
    n7["frontend/src/components/tasks/TaskForm.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/taskEditorContract.md"
    click n1 "../modules/taskDraftStorage.md"
    click n2 "../modules/taskDraftStorage.md"
    click n3 "../modules/taskEditorContract.md"
    click n4 "../modules/taskEditorContract.md"
    click n5 "../modules/taskEditorContract.md"
    click n6 "../modules/taskEditorContract.md"
    click n7 "../modules/TaskForm.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [taskEditorContract](../modules/taskEditorContract.md) | 0 | `assignee_id`, `depends_on`, `description`, `effort_days`, `effort_hours`, `expected_version`, `external_key`, `is_deferred`, `is_optional`, `max_end_date`, `milestone_id`, `min_start_date` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `readTaskDraft` | type_reference | [taskDraftStorage](../modules/taskDraftStorage.md) | — |
| `writeTaskDraft` | type_reference | [taskDraftStorage](../modules/taskDraftStorage.md) | — |
| `buildTaskEditorDefaults` | type_reference | [taskEditorContract](../modules/taskEditorContract.md) | — |
| `toTaskCreate` | type_reference | [taskEditorContract](../modules/taskEditorContract.md) | — |
| `toTaskUpdate` | type_reference | [taskEditorContract](../modules/taskEditorContract.md) | — |
| `validateTaskEditor` | type_reference | [taskEditorContract](../modules/taskEditorContract.md) | — |
| `TaskForm` | import | [TaskForm](../modules/TaskForm.md) | — |
