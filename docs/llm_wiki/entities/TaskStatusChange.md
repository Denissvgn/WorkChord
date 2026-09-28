# TaskStatusChange

**Location:** `backend/app/schemas/task.py:376`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task](../modules/schemas_task.md)

## Description

Request for changing task status.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `status` | `TaskStatus` | `status` | Yes | No | — | — | — | — |
| `reason` | `Optional[str]` | `reason` | No | Yes | `None` | max_length=500 | — | Reason for status change |
| `expected_version` | `Optional[int]` | `expected_version` | No | Yes | `None` | ge=1 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskStatusChange (backend/app/schemas/task.py)"]
    n1["BaseModel"]
    n2["change_task_status (backend/app/routers/tasks.py)"]
    n3["backend/tests/test_client_contract.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_task.md"
    click n2 "../modules/tasks.md"
    click n3 "../modules/test_client_contract.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task](../modules/schemas_task.md) | 0 | `expected_version`, `reason`, `status` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `change_task_status` | type_reference | [tasks](../modules/tasks.md) | — |
| `test_client_contract` | import | [test_client_contract](../modules/test_client_contract.md) | — |
