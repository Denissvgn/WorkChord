# UnscheduledTask

**Location:** `backend/app/schemas/gantt.py:82`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_gantt](../modules/schemas_gantt.md)

## Description

A planned task the scheduler left without dates, and what would change that.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task_id` | `int` | `task_id` | Yes | No | — | — | — | — |
| `task_title` | `str` | `task_title` | Yes | No | — | — | — | — |
| `reason` | `UnscheduledReason` | `reason` | Yes | No | — | — | — | — |
| `message` | `str` | `message` | Yes | No | — | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["UnscheduledTask (backend/app/schemas/gantt.py)"]
    n1["BaseModel"]
    n2["SchedulerService._unscheduled_tasks (backend/app/services/scheduler_service.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_gantt.md"
    click n2 "../modules/scheduler_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_gantt](../modules/schemas_gantt.md) | 0 | `message`, `reason`, `task_id`, `task_title` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `SchedulerService._unscheduled_tasks` | call | [scheduler_service](../modules/scheduler_service.md) | 1 |
| `SchedulerService._unscheduled_tasks` | type_reference | [scheduler_service](../modules/scheduler_service.md) | — |
