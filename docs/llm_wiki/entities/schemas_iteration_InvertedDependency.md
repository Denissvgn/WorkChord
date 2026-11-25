# InvertedDependency

**Location:** `backend/app/schemas/iteration.py:130`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_iteration](../modules/schemas_iteration.md)

## Description

A saved dependency whose dates start the dependent on or before its prerequisite's last day.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task_id` | `int` | `task_id` | Yes | No | — | — | — | — |
| `task_title` | `str` | `task_title` | Yes | No | — | — | — | — |
| `task_start_date` | `date` | `task_start_date` | Yes | No | — | — | — | — |
| `prerequisite_id` | `int` | `prerequisite_id` | Yes | No | — | — | — | — |
| `prerequisite_title` | `str` | `prerequisite_title` | Yes | No | — | — | — | — |
| `prerequisite_end_date` | `date` | `prerequisite_end_date` | Yes | No | — | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["InvertedDependency (backend/app/schemas/iteration.py)"]
    n1["BaseModel"]
    n2["backend/app/schemas/gantt.py"]
    n3["inverted_saved_dependencies (backend/app/services/dependency_order.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_iteration.md"
    click n2 "../modules/schemas_gantt.md"
    click n3 "../modules/dependency_order.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_iteration](../modules/schemas_iteration.md) | 0 | `prerequisite_end_date`, `prerequisite_id`, `prerequisite_title`, `task_id`, `task_start_date`, `task_title` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `gantt` | import | [schemas_gantt](../modules/schemas_gantt.md) | — |
| `inverted_saved_dependencies` | call | [dependency_order](../modules/dependency_order.md) | 1 |
| `inverted_saved_dependencies` | type_reference | [dependency_order](../modules/dependency_order.md) | — |
