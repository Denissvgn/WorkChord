# ScheduleResult

**Location:** `backend/app/schemas/gantt.py:76`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_gantt](../modules/schemas_gantt.md)

## Description

Result of scheduling operation.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `success` | `bool` | `success` | Yes | No | — | — | — | — |
| `decisions` | `list[SchedulingDecision]` | `decisions` | No | No | `[]` | — | — | — |
| `workload_balanced` | `bool` | `workload_balanced` | No | No | `True` | — | — | — |
| `workload_issues` | `list[WorkloadIssue]` | `workload_issues` | No | No | `[]` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ScheduleResult (backend/app/schemas/gantt.py)"]
    n1["BaseModel"]
    n2["schedule_iteration (backend/app/routers/gantt.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["SchedulerService.schedule_iteration (backend/app/services/scheduler_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_gantt.md"
    click n2 "../modules/routers_gantt.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/scheduler_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_gantt](../modules/schemas_gantt.md) | 0 | `decisions`, `success`, `workload_balanced`, `workload_issues` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `schedule_iteration` | type_reference | [routers_gantt](../modules/routers_gantt.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `SchedulerService.schedule_iteration` | call | [scheduler_service](../modules/scheduler_service.md) | 2 |
| `SchedulerService.schedule_iteration` | type_reference | [scheduler_service](../modules/scheduler_service.md) | — |
