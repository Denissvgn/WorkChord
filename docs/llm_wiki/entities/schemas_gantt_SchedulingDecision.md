# SchedulingDecision

**Location:** `backend/app/schemas/gantt.py:58`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_gantt](../modules/schemas_gantt.md)

## Description

Explanation for a scheduling decision.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task_id` | `int` | `task_id` | Yes | No | — | — | — | — |
| `task_title` | `str` | `task_title` | Yes | No | — | — | — | — |
| `decision_type` | `Literal['scheduled', 'reordered', 'delayed', 'overdue']` | `decision_type` | Yes | No | — | — | — | — |
| `reason` | `str` | `reason` | Yes | No | — | — | — | — |
| `affected_tasks` | `list[int]` | `affected_tasks` | No | No | `[]` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SchedulingDecision (backend/app/schemas/gantt.py)"]
    n1["BaseModel"]
    n2["_task_to_gantt (backend/app/routers/gantt.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["LLMService._enhance_explanation (backend/app/services/llm_service.py)"]
    n5["LLMService._schedule_explanation_fallback (backend/app/services/llm_service.py)"]
    n6["LLMService._schedule_recommendations (backend/app/services/llm_service.py)"]
    n7["LLMService.explain_schedule (backend/app/services/llm_service.py)"]
    n8["SchedulerService._schedule_composite_task (backend/app/services/scheduler_service.py)"]
    n9["SchedulerService._schedule_leaf_task (backend/app/services/scheduler_service.py)"]
    n10["SchedulerService._update_composite_task_dates (backend/app/services/scheduler_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    click n0 "../modules/schemas_gantt.md"
    click n2 "../modules/routers_gantt.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/llm_service.md"
    click n5 "../modules/llm_service.md"
    click n6 "../modules/llm_service.md"
    click n7 "../modules/llm_service.md"
    click n8 "../modules/scheduler_service.md"
    click n9 "../modules/scheduler_service.md"
    click n10 "../modules/scheduler_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_gantt](../modules/schemas_gantt.md) | 0 | `affected_tasks`, `decision_type`, `reason`, `task_id`, `task_title` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_task_to_gantt` | type_reference | [routers_gantt](../modules/routers_gantt.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `LLMService._enhance_explanation` | type_reference | [llm_service](../modules/llm_service.md) | — |
| `LLMService._schedule_explanation_fallback` | type_reference | [llm_service](../modules/llm_service.md) | — |
| `LLMService._schedule_recommendations` | type_reference | [llm_service](../modules/llm_service.md) | — |
| `LLMService.explain_schedule` | type_reference | [llm_service](../modules/llm_service.md) | — |
| `SchedulerService._schedule_composite_task` | call | [scheduler_service](../modules/scheduler_service.md) | 1 |
| `SchedulerService._schedule_composite_task` | type_reference | [scheduler_service](../modules/scheduler_service.md) | — |
| `SchedulerService._schedule_leaf_task` | call | [scheduler_service](../modules/scheduler_service.md) | 1 |
| `SchedulerService._schedule_leaf_task` | type_reference | [scheduler_service](../modules/scheduler_service.md) | — |
| `SchedulerService._update_composite_task_dates` | call | [scheduler_service](../modules/scheduler_service.md) | 1 |
| `SchedulerService._update_composite_task_dates` | type_reference | [scheduler_service](../modules/scheduler_service.md) | — |
