# TaskProject

**Location:** `backend/app/schemas/task.py:145`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task](../modules/schemas_task.md)

## Description

Brief project info for task.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `from_attributes` | `True` | config_class |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `id` | `int` | `id` | Yes | No | — | — | — | — |
| `name` | `str` | `name` | Yes | No | — | — | — | — |
| `status` | `str` | `status` | Yes | No | — | — | — | — |
| `health` | `str` | `health` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskProject (backend/app/schemas/task.py)"]
    n1["BaseModel"]
    n2["backend/app/schemas/__init__.py"]
    n3["TaskService.task_to_response (backend/app/services/task_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_task.md"
    click n2 "../modules/schemas___init__.md"
    click n3 "../modules/task_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task](../modules/schemas_task.md) | 0 | `health`, `id`, `name`, `status` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `TaskService.task_to_response` | call | [task_service](../modules/task_service.md) | 1 |
