# MetricMatchPage

**Location:** `backend/app/routers/task_domain.py:103`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [routers_task_domain](../modules/routers_task_domain.md)

## Description

_Auto-generated from `MetricMatchPage` in `backend/app/routers/task_domain.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `metric` | `str` | `metric` | Yes | No | — | — | — | — |
| `items` | `list[MetricMatchItem]` | `items` | Yes | No | — | — | — | — |
| `has_more` | `bool` | `has_more` | Yes | No | — | — | — | — |
| `next_after_id` | `int \| None` | `next_after_id` | No | Yes | `None` | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MetricMatchPage (backend/app/routers/task_domain.py)"]
    n1["BaseModel"]
    n2["metric_matches (backend/app/routers/task_domain.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/routers_task_domain.md"
    click n2 "../modules/routers_task_domain.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [routers_task_domain](../modules/routers_task_domain.md) | 0 | `has_more`, `items`, `metric`, `next_after_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `metric_matches` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
