# TaskTimelineItem

**Location:** `frontend/src/types/task.ts:384`
**Kind:** Class
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskTimelineItem` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `item_type` | `'task_event' \| 'status_log' \| 'agent_run' \| 'agent_run_event'` | Yes | — | — |
| `timestamp` | `string` | Yes | — | — |
| `title` | `string` | Yes | — | — |
| `payload` | `Record<string, unknown>` | Yes | — | — |
| `actor_type` | `string \| null` | No | — | — |
| `actor_id` | `number \| null` | No | — | — |
| `trace_id` | `string \| null` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `actor_id`, `actor_type`, `item_type`, `payload`, `timestamp`, `title`, `trace_id` |
