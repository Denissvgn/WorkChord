# TaskTimelineItem

**Location:** `frontend/src/types/task.ts:330`
**Kind:** Class
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskTimelineItem` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `item_type` | `'task_event' \| 'status_log' \| 'agent_run' \| 'agent_run_event'` | *required* | — |
| `timestamp` | `string` | *required* | — |
| `title` | `string` | *required* | — |
| `payload` | `Record<string, unknown>` | *required* | — |
| `actor_type` | `string \| null` | *required* | — |
| `actor_id` | `number \| null` | *required* | — |
| `trace_id` | `string \| null` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `actor_id`, `actor_type`, `item_type`, `payload`, `timestamp`, `title`, `trace_id` |
