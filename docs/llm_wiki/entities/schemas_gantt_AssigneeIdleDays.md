# AssigneeIdleDays

**Location:** `backend/app/schemas/gantt.py:165`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_gantt](../modules/schemas_gantt.md)

## Description

An assignee's working days left idle inside the scheduled span, before the row's last work.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `member_id` | `int` | `member_id` | Yes | No | — | — | — | — |
| `member_name` | `str` | `member_name` | Yes | No | — | — | — | — |
| `idle_working_days` | `int` | `idle_working_days` | Yes | No | — | — | — | — |
| `gaps` | `list[IdleGap]` | `gaps` | Yes | No | — | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AssigneeIdleDays (backend/app/schemas/gantt.py)"]
    n1["BaseModel"]
    n2["SchedulerService._idle_days (backend/app/services/scheduler_service.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_gantt.md"
    click n2 "../modules/scheduler_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_gantt](../modules/schemas_gantt.md) | 0 | `gaps`, `idle_working_days`, `member_id`, `member_name` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `SchedulerService._idle_days` | call | [scheduler_service](../modules/scheduler_service.md) | 1 |
| `SchedulerService._idle_days` | type_reference | [scheduler_service](../modules/scheduler_service.md) | — |
