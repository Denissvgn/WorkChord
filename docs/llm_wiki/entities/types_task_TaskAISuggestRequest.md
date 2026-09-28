# TaskAISuggestRequest

**Location:** `frontend/src/types/task.ts:233`
**Kind:** Class
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskAISuggestRequest` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `brief` | `TaskBrief \| null` | No | — | — |
| `title` | `string` | Yes | — | — |
| `description` | `string \| null` | No | — | — |
| `priority` | `number \| null` | No | — | — |
| `effort_days` | `number \| null` | No | — | — |
| `effort_hours` | `number \| null` | No | — | — |
| `assignee_id` | `number \| null` | No | — | — |
| `project_id` | `number \| null` | No | — | — |
| `milestone_id` | `number \| null` | No | — | — |
| `parent_id` | `number \| null` | No | — | — |
| `depends_on` | `number[]` | No | — | — |
| `tags` | `string[]` | No | — | — |
| `is_optional` | `boolean \| null` | No | — | — |
| `is_deferred` | `boolean \| null` | No | — | — |
| `min_start_date` | `string \| null` | No | — | — |
| `max_end_date` | `string \| null` | No | — | — |
| `source` | `string \| null` | No | — | — |
| `source_url` | `string \| null` | No | — | — |
| `external_key` | `string \| null` | No | — | — |
| `template_id` | `number \| null` | No | — | — |
| `user_context` | `string \| null` | No | — | — |
| `extra_context` | `Record<string, unknown>` | No | — | — |

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
| [types_task](../modules/types_task.md) | 0 | `assignee_id`, `brief`, `depends_on`, `description`, `effort_days`, `effort_hours`, `external_key`, `extra_context`, `is_deferred`, `is_optional`, `max_end_date`, `milestone_id` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskForm` | import | [TaskForm](../modules/TaskForm.md) | — |
| `taskService` | import | [taskService](../modules/taskService.md) | — |
