# BacklogRestoreRequest

**Location:** `backend/app/schemas/task_domain.py:50`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task_domain](../modules/schemas_task_domain.md)

## Description

_Auto-generated from `BacklogRestoreRequest` in `backend/app/schemas/task_domain.py`._

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `expected_versions` | `dict[int, int]` | `expected_versions` | Yes | No | — | — | — | — |
| `reason` | `str` | `reason` | Yes | No | — | max_length=2000; min_length=1 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["BacklogRestoreRequest (backend/app/schemas/task_domain.py)"]
    n1["BaseModel"]
    n2["restore_backlog (backend/app/routers/task_domain.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_task_domain.md"
    click n2 "../modules/routers_task_domain.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task_domain](../modules/schemas_task_domain.md) | 0 | `expected_versions`, `reason` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `restore_backlog` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
