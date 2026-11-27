# IdleGap

**Location:** `backend/app/schemas/gantt.py:149`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_gantt](../modules/schemas_gantt.md)

## Description

Working days an assignee is left idle before the task that follows them on the row.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `start_date` | `date` | `start_date` | Yes | No | — | — | — | — |
| `end_date` | `date` | `end_date` | Yes | No | — | — | — | — |
| `working_days` | `int` | `working_days` | Yes | No | — | — | — | — |
| `task_id` | `int` | `task_id` | Yes | No | — | — | — | — |
| `task_title` | `str` | `task_title` | Yes | No | — | — | — | — |
| `reason` | `IdleReason` | `reason` | Yes | No | — | — | — | — |
| `waiting_on` | `WaitingOnTask \| None` | `waiting_on` | No | Yes | `None` | — | — | — |
| `earliest_start` | `date \| None` | `earliest_start` | No | Yes | `None` | — | — | — |
| `message` | `str` | `message` | Yes | No | — | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["IdleGap (backend/app/schemas/gantt.py)"]
    n1["BaseModel"]
    n2["SchedulerService._idle_gap (backend/app/services/scheduler_service.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_gantt.md"
    click n2 "../modules/scheduler_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_gantt](../modules/schemas_gantt.md) | 0 | `earliest_start`, `end_date`, `message`, `reason`, `start_date`, `task_id`, `task_title`, `waiting_on`, `working_days` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `SchedulerService._idle_gap` | call | [scheduler_service](../modules/scheduler_service.md) | 1 |
| `SchedulerService._idle_gap` | type_reference | [scheduler_service](../modules/scheduler_service.md) | — |
