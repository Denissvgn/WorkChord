# TaskReference

**Location:** `backend/app/schemas/task_detail.py:9`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [task_detail](../modules/task_detail.md)

## Description

_Auto-generated from `TaskReference` in `backend/app/schemas/task_detail.py`._

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `from_attributes` | `True` | model_config |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `id` | `int` | `id` | Yes | No | — | — | — | — |
| `title` | `str` | `title` | Yes | No | — | — | — | — |
| `version` | `int` | `version` | Yes | No | — | — | — | — |
| `status` | `str` | `status` | Yes | No | — | — | — | — |
| `project_id` | `int \| None` | `project_id` | Yes | Yes | — | — | — | — |
| `iteration_id` | `int \| None` | `iteration_id` | Yes | Yes | — | — | — | — |
| `parent_id` | `int \| None` | `parent_id` | Yes | Yes | — | — | — | — |
| `owner_profile_id` | `int \| None` | `owner_profile_id` | Yes | Yes | — | — | — | — |
| `project_name` | `str \| None` | `project_name` | No | Yes | `None` | — | — | — |
| `iteration_name` | `str \| None` | `iteration_name` | No | Yes | `None` | — | — | — |
| `blocked_reason` | `str \| None` | `blocked_reason` | No | Yes | `None` | — | — | — |
| `canceled_at` | `datetime \| None` | `canceled_at` | No | Yes | `None` | — | — | — |
| `acceptance_current` | `bool` | `acceptance_current` | No | No | `False` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskReference (backend/app/schemas/task_detail.py)"]
    n1["BaseModel"]
    n2["HumanWorkReference (backend/app/schemas/task_detail.py)"]
    n3["backend/app/services/task_detail_service.py"]
    n4["build_examples (scripts/generate_mobile_contract_fixtures.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/task_detail.md"
    click n2 "../modules/task_detail.md"
    click n3 "../modules/task_detail_service.md"
    click n4 "../modules/generate_mobile_contract_fixtures.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [task_detail](../modules/task_detail.md) | 0 | `acceptance_current`, `blocked_reason`, `canceled_at`, `id`, `iteration_id`, `iteration_name`, `owner_profile_id`, `parent_id`, `project_id`, `project_name`, `status`, `title` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
| Subclass | `HumanWorkReference` | [task_detail](../modules/task_detail.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `task_detail_service` | import | [task_detail_service](../modules/task_detail_service.md) | — |
| `build_examples` | call | [generate_mobile_contract_fixtures](../modules/generate_mobile_contract_fixtures.md) | 1 |
