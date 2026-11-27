# TaskPostponementResponse

**Location:** `backend/app/schemas/task_postponement.py:137`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task_postponement](../modules/schemas_task_postponement.md)

## Description

_Auto-generated from `TaskPostponementResponse` in `backend/app/schemas/task_postponement.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task` | `TaskResponse` | `task` | Yes | No | — | — | — | — |
| `postponement` | `TaskPostponementRecord \| None` | `postponement` | Yes | Yes | — | — | — | The open or most recent postponement; null only for work reactivated from a postponed state that had no record. |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskPostponementResponse (backend/app/schemas/task_postponement.py)"]
    n1["BaseModel"]
    n2["postpone_task (backend/app/routers/task_domain.py)"]
    n3["reactivate_task (backend/app/routers/task_domain.py)"]
    n4["task_postponement (backend/app/routers/task_domain.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_task_postponement.md"
    click n2 "../modules/routers_task_domain.md"
    click n3 "../modules/routers_task_domain.md"
    click n4 "../modules/routers_task_domain.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task_postponement](../modules/schemas_task_postponement.md) | 0 | `postponement`, `task` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `postpone_task` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `reactivate_task` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `task_postponement` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
