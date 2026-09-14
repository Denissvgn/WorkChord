# TaskBulkOperationRequest

**Location:** `backend/app/schemas/task.py:250`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task](../modules/schemas_task.md)

## Description

Request schema for selected-task bulk operations.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task_ids` | `list[int]` | `task_ids` | Yes | No | — | min_length=1; max_length=200 | — | — |
| `action` | `TaskBulkAction` | `action` | Yes | No | — | — | — | — |
| `payload` | `dict[str, Any]` | `payload` | No | No | factory: `dict` | — | — | — |
| `dry_run` | `bool` | `dry_run` | No | No | `True` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskBulkOperationRequest (backend/app/schemas/task.py)"]
    n1["BaseModel"]
    n2["run_task_bulk_operation (backend/app/routers/tasks.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["TaskBulkOperationService._build_update (backend/app/services/task_bulk_operation_service.py)"]
    n5["TaskBulkOperationService._run_for_task (backend/app/services/task_bulk_operation_service.py)"]
    n6["TaskBulkOperationService.run (backend/app/services/task_bulk_operation_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/schemas_task.md"
    click n2 "../modules/tasks.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/task_bulk_operation_service.md"
    click n5 "../modules/task_bulk_operation_service.md"
    click n6 "../modules/task_bulk_operation_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task](../modules/schemas_task.md) | 0 | `action`, `dry_run`, `payload`, `task_ids` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `run_task_bulk_operation` | type_reference | [tasks](../modules/tasks.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `TaskBulkOperationService._build_update` | type_reference | [task_bulk_operation_service](../modules/task_bulk_operation_service.md) | — |
| `TaskBulkOperationService._run_for_task` | type_reference | [task_bulk_operation_service](../modules/task_bulk_operation_service.md) | — |
| `TaskBulkOperationService.run` | type_reference | [task_bulk_operation_service](../modules/task_bulk_operation_service.md) | — |
