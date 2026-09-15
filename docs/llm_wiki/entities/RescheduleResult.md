# RescheduleResult

**Location:** `backend/app/services/scheduler_service.py:51`
**Kind:** Class
**Bases:** —
**Module:** [scheduler_service](../modules/scheduler_service.md)

**Decorators:** `@dataclass`

## Description

Result of an incremental reschedule operation.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `affected_task_ids` | `list[int]` | *required* | — |
| `rescheduled_count` | `int` | *required* | — |
| `decisions` | `list[SchedulingDecision]` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RescheduleResult (backend/app/services/scheduler_service.py)"]
    n1["IncrementalScheduler._reschedule_subset (backend/app/services/scheduler_service.py)"]
    n2["IncrementalScheduler.reschedule_affected (backend/app/services/scheduler_service.py)"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/scheduler_service.md"
    click n1 "../modules/scheduler_service.md"
    click n2 "../modules/scheduler_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [scheduler_service](../modules/scheduler_service.md) | 0 | `affected_task_ids`, `decisions`, `rescheduled_count` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `IncrementalScheduler._reschedule_subset` | call | [scheduler_service](../modules/scheduler_service.md) | 3 |
| `IncrementalScheduler._reschedule_subset` | type_reference | [scheduler_service](../modules/scheduler_service.md) | — |
| `IncrementalScheduler.reschedule_affected` | call | [scheduler_service](../modules/scheduler_service.md) | 1 |
| `IncrementalScheduler.reschedule_affected` | type_reference | [scheduler_service](../modules/scheduler_service.md) | — |
