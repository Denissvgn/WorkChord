# GroundedAISuggestionResponse

**Location:** `frontend/src/types/task.ts:258`
**Kind:** Class
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `GroundedAISuggestionResponse` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `provider` | `string \| null` | No | — | — |
| `model` | `string \| null` | No | — | — |
| `language` | `'en' \| 'ru'` | No | — | — |
| `is_fallback` | `boolean` | Yes | — | — |
| `finish_reason` | `string \| null` | No | — | — |
| `is_truncated` | `boolean` | Yes | — | — |
| `suggested_title` | `string \| null` | No | — | — |
| `suggested_description` | `string` | Yes | — | — |
| `acceptance_criteria` | `string[]` | Yes | — | — |
| `implementation_notes` | `string[]` | Yes | — | — |
| `risks` | `string[]` | Yes | — | — |
| `open_questions` | `string[]` | Yes | — | — |
| `grounded_facts` | `GroundedFact[]` | Yes | — | — |
| `ungrounded_suggestions` | `string[]` | Yes | — | — |
| `warnings` | `string[]` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GroundedAISuggestionResponse (frontend/src/types/task.ts)"]
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
| [types_task](../modules/types_task.md) | 0 | `acceptance_criteria`, `finish_reason`, `grounded_facts`, `implementation_notes`, `is_fallback`, `is_truncated`, `language`, `model`, `open_questions`, `provider`, `risks`, `suggested_description` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskForm` | import | [TaskForm](../modules/TaskForm.md) | — |
| `taskService` | import | [taskService](../modules/taskService.md) | — |
