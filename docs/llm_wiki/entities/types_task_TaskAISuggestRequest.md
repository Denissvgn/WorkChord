# TaskAISuggestRequest

**Location:** `frontend/src/types/task.ts:212`
**Kind:** Class
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskAISuggestRequest` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `string` | *required* | — |
| `description` | `string \| null` | *required* | — |
| `priority` | `number \| null` | *required* | — |
| `effort_days` | `number \| null` | *required* | — |
| `effort_hours` | `number \| null` | *required* | — |
| `assignee_id` | `number \| null` | *required* | — |
| `project_id` | `number \| null` | *required* | — |
| `milestone_id` | `number \| null` | *required* | — |
| `parent_id` | `number \| null` | *required* | — |
| `depends_on` | `number[]` | *required* | — |
| `tags` | `string[]` | *required* | — |
| `is_optional` | `boolean \| null` | *required* | — |
| `is_deferred` | `boolean \| null` | *required* | — |
| `min_start_date` | `string \| null` | *required* | — |
| `max_end_date` | `string \| null` | *required* | — |
| `source` | `string \| null` | *required* | — |
| `source_url` | `string \| null` | *required* | — |
| `external_key` | `string \| null` | *required* | — |
| `template_id` | `number \| null` | *required* | — |
| `user_context` | `string \| null` | *required* | — |
| `extra_context` | `Record<string, unknown>` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskAISuggestRequest (frontend/src/types/task.ts)"]
    n1["frontend/src/components/tasks/TaskForm.tsx"]
    n2["frontend/src/services/taskService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/TaskForm.md"
    click n2 "../modules/taskService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `assignee_id`, `depends_on`, `description`, `effort_days`, `effort_hours`, `external_key`, `extra_context`, `is_deferred`, `is_optional`, `max_end_date`, `milestone_id`, `min_start_date` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskForm` | import | [TaskForm](../modules/TaskForm.md) | — |
| `taskService` | import | [taskService](../modules/taskService.md) | — |
