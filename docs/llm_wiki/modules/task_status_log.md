# task_status_log Module

**Path:** `backend/app/models/task_status_log.py`

## Description

Task status log model for audit trail.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.models.task` | `Task` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `ForeignKey`, `Integer`, `String`, `Text` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column`, `relationship` |
| `typing` | `TYPE_CHECKING`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/task.py"]
    n3["backend/app/models/task_status_log.py"]
    n4["backend/app/services/task_status_service.py"]
    n5["backend/app/services/task_timeline_service.py"]
    n6["backend/app/utils/time.py"]
    n7["backend/tests/test_effective_deferral.py"]
    n8["backend/tests/test_task_pagination.py"]
    n1 --> n2
    n1 --> n3
    n2 --> n0
    n2 --> n3
    n2 --> n6
    n3 --> n0
    n3 --> n2
    n3 --> n6
    n4 --> n2
    n4 --> n3
    n5 --> n2
    n5 --> n3
    n5 --> n6
    n7 --> n2
    n7 --> n3
    n8 --> n2
    n8 --> n3
    n8 --> n5
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_task.md"
    click n3 "../modules/task_status_log.md"
    click n4 "../modules/task_status_service.md"
    click n5 "../modules/task_timeline_service.md"
    click n6 "../modules/time.md"
    click n7 "../modules/test_effective_deferral.md"
    click n8 "../modules/test_task_pagination.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [models_task](../modules/models_task.md) |
| Inbound | [task_status_service](../modules/task_status_service.md) |
| Inbound | [task_timeline_service](../modules/task_timeline_service.md) |
| Inbound | [test_effective_deferral](../modules/test_effective_deferral.md) |
| Inbound | [test_task_pagination](../modules/test_task_pagination.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskStatusLog](../entities/task_status_log_TaskStatusLog.md) | 15 | `Base` | Audit log for task status changes. |
