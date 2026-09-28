# IterationSeriesCreate

**Location:** `backend/app/schemas/iteration.py:48`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_iteration](../modules/schemas_iteration.md)

## Description

Schema for creating multiple back-to-back iterations.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `base_name` | `str` | `base_name` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `calendar_id` | `Optional[int]` | `calendar_id` | No | Yes | `None` | — | — | — |
| `project_id` | `Optional[int]` | `project_id` | No | Yes | `None` | — | — | — |
| `start_date` | `date` | `start_date` | Yes | No | — | — | — | — |
| `duration_days` | `int` | `duration_days` | No | No | `14` | ge=1; le=366 | — | — |
| `stop` | `IterationSeriesStop` | `stop` | Yes | No | — | — | — | — |
| `manager_email` | `Optional[str]` | `manager_email` | No | Yes | `None` | max_length=255 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["IterationSeriesCreate (backend/app/schemas/iteration.py)"]
    n1["BaseModel"]
    n2["create_iteration_series (backend/app/routers/iterations.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["IterationService._series_items (backend/app/services/iteration_service.py)"]
    n5["IterationService.create_series (backend/app/services/iteration_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/schemas_iteration.md"
    click n2 "../modules/iterations.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/iteration_service.md"
    click n5 "../modules/iteration_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_iteration](../modules/schemas_iteration.md) | 0 | `base_name`, `calendar_id`, `duration_days`, `manager_email`, `project_id`, `start_date`, `stop` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_iteration_series` | type_reference | [iterations](../modules/iterations.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `IterationService._series_items` | type_reference | [iteration_service](../modules/iteration_service.md) | — |
| `IterationService.create_series` | type_reference | [iteration_service](../modules/iteration_service.md) | — |
