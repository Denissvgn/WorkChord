# WorkloadIssue

**Location:** `backend/app/schemas/gantt.py:69`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_gantt](../modules/schemas_gantt.md)

## Description

Workload issue for a team member.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `member_id` | `int` | `member_id` | Yes | No | — | — | — | — |
| `member_name` | `str` | `member_name` | Yes | No | — | — | — | — |
| `issue` | `str` | `issue` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WorkloadIssue (backend/app/schemas/gantt.py)"]
    n1["BaseModel"]
    n2["_task_to_gantt (backend/app/routers/gantt.py)"]
    n3["LLMService._enhance_explanation (backend/app/services/llm_service.py)"]
    n4["LLMService._schedule_explanation_fallback (backend/app/services/llm_service.py)"]
    n5["LLMService._schedule_recommendations (backend/app/services/llm_service.py)"]
    n6["LLMService.explain_schedule (backend/app/services/llm_service.py)"]
    n7["SchedulerService._check_workload_balance (backend/app/services/scheduler_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/schemas_gantt.md"
    click n2 "../modules/routers_gantt.md"
    click n3 "../modules/llm_service.md"
    click n4 "../modules/llm_service.md"
    click n5 "../modules/llm_service.md"
    click n6 "../modules/llm_service.md"
    click n7 "../modules/scheduler_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_gantt](../modules/schemas_gantt.md) | 0 | `issue`, `member_id`, `member_name` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_task_to_gantt` | type_reference | [routers_gantt](../modules/routers_gantt.md) | — |
| `LLMService._enhance_explanation` | type_reference | [llm_service](../modules/llm_service.md) | — |
| `LLMService._schedule_explanation_fallback` | type_reference | [llm_service](../modules/llm_service.md) | — |
| `LLMService._schedule_recommendations` | type_reference | [llm_service](../modules/llm_service.md) | — |
| `LLMService.explain_schedule` | type_reference | [llm_service](../modules/llm_service.md) | — |
| `SchedulerService._check_workload_balance` | call | [scheduler_service](../modules/scheduler_service.md) | 1 |
| `SchedulerService._check_workload_balance` | type_reference | [scheduler_service](../modules/scheduler_service.md) | — |
