# TaskEditorValues

**Location:** `frontend/src/components/tasks/taskEditorContract.ts:10`
**Kind:** Class
**Bases:** —
**Module:** [taskEditorContract](../modules/taskEditorContract.md)

## Description

_Auto-generated from `TaskEditorValues` in `frontend/src/components/tasks/taskEditorContract.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `title` | `string` | Yes | — | — |
| `description` | `string` | Yes | — | — |
| `priority` | `number` | Yes | — | — |
| `effort_days` | `number \| null` | Yes | — | — |
| `effort_hours` | `number \| null` | Yes | — | — |
| `owner_profile_id` | `number \| null` | Yes | — | — |
| `brief` | `TaskBrief \| null` | Yes | — | — |
| `estimate_provenance` | `"unknown" \| "assumed" \| "estimated"` | Yes | — | — |
| `assignee_id` | `number \| null` | Yes | — | — |
| `project_id` | `number \| null` | Yes | — | — |
| `milestone_id` | `number \| null` | Yes | — | — |
| `parent_id` | `number \| null` | Yes | — | — |
| `depends_on` | `number[]` | Yes | — | — |
| `is_optional` | `boolean` | Yes | — | — |
| `is_deferred` | `boolean` | Yes | — | — |
| `tags` | `string[]` | Yes | — | — |
| `min_start_date` | `string \| null` | Yes | — | — |
| `max_end_date` | `string \| null` | Yes | — | — |
| `external_key` | `string \| null` | Yes | — | — |
| `source` | `string \| null` | Yes | — | — |
| `source_url` | `string \| null` | Yes | — | — |
| `status` | `TaskStatus` | Yes | — | — |
| `expected_version` | `number \| null` | Yes | — | — |
| `expected_revision` | `number \| null` | Yes | — | — |

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
| [taskEditorContract](../modules/taskEditorContract.md) | 0 | `assignee_id`, `brief`, `depends_on`, `description`, `effort_days`, `effort_hours`, `estimate_provenance`, `expected_revision`, `expected_version`, `external_key`, `is_deferred`, `is_optional` |

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
