# TimeReport

**Location:** `frontend/src/services/timeEntryService.ts:10`
**Kind:** Class
**Bases:** —
**Module:** [timeEntryService](../modules/timeEntryService.md)

## Description

_Auto-generated from `TimeReport` in `frontend/src/services/timeEntryService.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `project_id` | `number` | Yes | — | — |
| `scope` | `'mine' \| 'project'` | Yes | — | — |
| `start` | `string` | Yes | — | — |
| `end` | `string` | Yes | — | — |
| `upper_id` | `number` | Yes | — | — |
| `has_more` | `boolean` | Yes | — | — |
| `next_after_id` | `number \| null` | Yes | — | — |
| `can_view_project_totals` | `boolean` | Yes | — | — |
| `items` | `{ task_id: number; task_title: string \| null; recorded_minutes: number \| null; entry_count: number;         estimate_hours: number \| null; estimate_state: 'known' \| 'unknown' \| 'unavailable' }[]` | Yes | — | — |
| `totals` | `{ task_count: number; tasks_with_records: number; recorded_minutes: number \| null;         project_work_minutes: number \| null; known_estimate_hours: number \| null; tasks_with_estimates: number }` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [timeEntryService](../modules/timeEntryService.md) | 0 | `can_view_project_totals`, `end`, `has_more`, `items`, `next_after_id`, `project_id`, `scope`, `start`, `totals`, `upper_id` |
