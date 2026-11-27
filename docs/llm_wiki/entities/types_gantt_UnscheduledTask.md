# UnscheduledTask

**Location:** `frontend/src/types/gantt.ts:90`
**Kind:** Interface
**Bases:** —
**Module:** [types_gantt](../modules/types_gantt.md)

## Description

A planned task the scheduler left without dates, with the cause and the server's English hint.

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `task_id` | `number` | Yes | — | — |
| `task_title` | `string` | Yes | — | — |
| `reason` | `UnscheduledReason` | Yes | — | — |
| `message` | `string` | Yes | — | — |
| `dates_cleared` | `boolean` | No | — | — |
| `date_rule` | `DateRule` | No | — | — |
| `also` | `UnscheduledReason[]` | No | — | — |
| `waiting_on` | `WaitingOnTask[]` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["UnscheduledTask (frontend/src/types/gantt.ts)"]
    n1["unscheduledReasonText (frontend/src/components/gantt/unscheduledReason.ts)"]
    n2["UnscheduledTasks (frontend/src/components/gantt/UnscheduledTasks.tsx)"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_gantt.md"
    click n1 "../modules/unscheduledReason.md"
    click n2 "../modules/UnscheduledTasks.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_gantt](../modules/types_gantt.md) | 0 | `also`, `date_rule`, `dates_cleared`, `message`, `reason`, `task_id`, `task_title`, `waiting_on` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `unscheduledReasonText` | type_reference | [unscheduledReason](../modules/unscheduledReason.md) | — |
| `UnscheduledTasks` | type_reference | [UnscheduledTasks](../modules/UnscheduledTasks.md) | — |
