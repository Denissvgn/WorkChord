# TaskTreeIntegrityError

**Location:** `backend/app/services/task_hierarchy_service.py:9`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [task_hierarchy_service](../modules/task_hierarchy_service.md)

## Description

Raised when persisted task parent links cannot form a valid iteration tree.

## Attributes

*No annotated attributes found.*

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskTreeIntegrityError (backend/app/services/task_hierarchy_service.py)"]
    n1["ValueError"]
    n2["backend/app/services/task_domain_service.py"]
    n3["backend/app/services/task_service.py"]
    n4["backend/app/services/task_status_service.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/task_hierarchy_service.md"
    click n2 "../modules/task_domain_service.md"
    click n3 "../modules/task_service.md"
    click n4 "../modules/task_status_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [task_hierarchy_service](../modules/task_hierarchy_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `task_domain_service` | import | [task_domain_service](../modules/task_domain_service.md) | — |
| `task_service` | import | [task_service](../modules/task_service.md) | — |
| `task_status_service` | import | [task_status_service](../modules/task_status_service.md) | — |
