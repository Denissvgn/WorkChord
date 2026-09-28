# TaskCreate

**Location:** `frontend/src/types/task.ts:163`
**Kind:** Class
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskCreate` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `owner_profile_id` | `number \| null` | No | — | — |
| `brief` | `TaskBrief` | No | — | — |
| `estimate_provenance` | `"unknown" \| "assumed" \| "estimated"` | No | — | — |
| `expected_revision` | `number` | No | — | — |
| `parent_id` | `number \| null` | No | — | — |
| `title` | `string` | Yes | — | — |
| `description` | `string` | No | — | — |
| `priority` | `number` | Yes | — | — |
| `effort_days` | `number \| null` | Yes | — | — |
| `effort_hours` | `number \| null` | No | — | — |
| `assignee_id` | `number \| null` | No | — | — |
| `project_id` | `number \| null` | No | — | — |
| `milestone_id` | `number \| null` | No | — | — |
| `depends_on` | `number[]` | Yes | — | — |
| `is_optional` | `boolean` | No | — | — |
| `is_deferred` | `boolean` | No | — | — |
| `tags` | `string[]` | No | — | — |
| `sort_order` | `number` | No | — | — |
| `min_start_date` | `string \| null` | No | — | — |
| `max_end_date` | `string \| null` | No | — | — |
| `external_key` | `string \| null` | No | — | — |
| `source` | `string \| null` | No | — | — |
| `source_url` | `string \| null` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskCreate (frontend/src/types/task.ts)"]
    n1["toTaskCreate (frontend/src/components/tasks/taskEditorContract.ts)"]
    n2["frontend/src/components/tasks/TaskForm.tsx"]
    n3["frontend/src/services/taskService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/taskEditorContract.md"
    click n2 "../modules/TaskForm.md"
    click n3 "../modules/taskService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `assignee_id`, `brief`, `depends_on`, `description`, `effort_days`, `effort_hours`, `estimate_provenance`, `expected_revision`, `external_key`, `is_deferred`, `is_optional`, `max_end_date` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `toTaskCreate` | type_reference | [taskEditorContract](../modules/taskEditorContract.md) | — |
| `TaskForm` | import | [TaskForm](../modules/TaskForm.md) | — |
| `taskService` | import | [taskService](../modules/taskService.md) | — |
