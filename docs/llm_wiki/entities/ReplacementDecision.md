# ReplacementDecision

**Location:** `backend/app/schemas/task_replacement.py:54`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task_replacement](../modules/schemas_task_replacement.md)

## Description

_Auto-generated from `ReplacementDecision` in `backend/app/schemas/task_replacement.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `reason` | `str` | `reason` | Yes | No | — | — | — | — |
| `owner_decision` | `str` | `owner_decision` | Yes | No | — | — | — | — |
| `decided_at` | `datetime` | `decided_at` | Yes | No | — | — | — | — |
| `decided_by_principal_id` | `int \| None` | `decided_by_principal_id` | No | Yes | `None` | — | — | — |
| `decided_by_actor_id` | `int \| None` | `decided_by_actor_id` | No | Yes | `None` | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ReplacementDecision (backend/app/schemas/task_replacement.py)"]
    n1["BaseModel"]
    n0 --> n1
    click n0 "../modules/schemas_task_replacement.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task_replacement](../modules/schemas_task_replacement.md) | 0 | `decided_at`, `decided_by_actor_id`, `decided_by_principal_id`, `owner_decision`, `reason` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
