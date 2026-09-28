# TaskImportDestination

**Location:** `backend/app/schemas/task.py:325`
**Kind:** Type alias
**Bases:** —
**Module:** [schemas_task](../modules/schemas_task.md)
**Target:** `Literal['tasks', 'triage', 'auto']`

## Description

_Auto-generated from `TaskImportDestination` in `backend/app/schemas/task.py`._

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskImportDestination (backend/app/schemas/task.py)"]
    n1["TaskImportService.bulk_update_tasks_from_text (backend/app/services/task_import_service.py)"]
    n2["TaskImportService.import_tasks (backend/app/services/task_import_service.py)"]
    n3["TaskService.bulk_update_tasks_from_text (backend/app/services/task_service.py)"]
    n4["TaskService.import_tasks (backend/app/services/task_service.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_task.md"
    click n1 "../modules/task_import_service.md"
    click n2 "../modules/task_import_service.md"
    click n3 "../modules/task_service.md"
    click n4 "../modules/task_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task](../modules/schemas_task.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskImportService.bulk_update_tasks_from_text` | type_reference | [task_import_service](../modules/task_import_service.md) | — |
| `TaskImportService.import_tasks` | type_reference | [task_import_service](../modules/task_import_service.md) | — |
| `TaskService.bulk_update_tasks_from_text` | type_reference | [task_service](../modules/task_service.md) | — |
| `TaskService.import_tasks` | type_reference | [task_service](../modules/task_service.md) | — |
