# TaskDeletionFence

**Location:** `backend/app/models/recovery.py:54`
**Kind:** Class
**Bases:** `Base`
**Module:** [recovery](../modules/recovery.md)

## Description

Retain the highest deleted task version independently of task lifetime.

The task deletion hook writes the highest observed task version to an independent table in the same ORM transaction, including cascaded children and removals during recovery. Rollback removes an uncommitted fence. A surviving fence protects later reuse of the task ID; the upgrade does not invent records for historical deletions.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `original_task_id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=False)` | — |
| `last_version` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskDeletionFence (backend/app/models/recovery.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["backend/app/services/task_recovery_service.py"]
    n4["backend/tests/test_task_domain_integrity.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/recovery.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/task_recovery_service.md"
    click n4 "../modules/test_task_domain_integrity.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [recovery](../modules/recovery.md) | 0 | `last_version`, `original_task_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `task_recovery_service` | import | [task_recovery_service](../modules/task_recovery_service.md) | — |
| `test_task_domain_integrity` | import | [test_task_domain_integrity](../modules/test_task_domain_integrity.md) | — |
