# WaitingOnTask

**Location:** `backend/app/schemas/gantt.py:99`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_gantt](../modules/schemas_gantt.md)

## Description

A task a planned task waits on: postponed work, or the prerequisite behind idle days.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task_id` | `int` | `task_id` | Yes | No | — | — | — | — |
| `task_title` | `str` | `task_title` | Yes | No | — | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WaitingOnTask (backend/app/schemas/gantt.py)"]
    n1["BaseModel"]
    n2["_no_waits (backend/app/schemas/gantt.py)"]
    n3["SchedulerService._idle_gap (backend/app/services/scheduler_service.py)"]
    n4["SchedulerService._unscheduled_tasks (backend/app/services/scheduler_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_gantt.md"
    click n2 "../modules/schemas_gantt.md"
    click n3 "../modules/scheduler_service.md"
    click n4 "../modules/scheduler_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_gantt](../modules/schemas_gantt.md) | 0 | `task_id`, `task_title` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_no_waits` | type_reference | [schemas_gantt](../modules/schemas_gantt.md) | — |
| `SchedulerService._idle_gap` | call | [scheduler_service](../modules/scheduler_service.md) | 1 |
| `SchedulerService._unscheduled_tasks` | call | [scheduler_service](../modules/scheduler_service.md) | 1 |
