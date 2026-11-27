# task_postponement Module

**Path:** `backend/app/models/task_postponement.py`

## Description

A recorded decision that stopped a task, and what must be true before it resumes.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `date`, `datetime` |
| `sqlalchemy` | `JSON`, `CheckConstraint`, `Date`, `ForeignKey`, `Index`, `Integer`, `String`, `Text`, `text` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/task_postponement.py"]
    n3["backend/app/services/task_postponement_service.py"]
    n4["backend/app/services/task_reactivation_service.py"]
    n5["backend/app/services/task_replacement_service.py"]
    n6["backend/app/utils/time.py"]
    n7["backend/tests/migrations/test_task_postponement_migration.py"]
    n8["backend/tests/test_task_postponement.py"]
    n9["backend/tests/test_task_reactivation.py"]
    n10["backend/tests/test_task_supersession.py"]
    n1 --> n2
    n2 --> n0
    n2 --> n6
    n3 --> n2
    n3 --> n4
    n3 --> n6
    n4 --> n0
    n4 --> n2
    n4 --> n3
    n4 --> n6
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n5 --> n6
    n7 --> n2
    n8 --> n2
    n8 --> n3
    n8 --> n6
    n9 --> n2
    n9 --> n3
    n9 --> n4
    n9 --> n6
    n9 --> n8
    n10 --> n2
    n10 --> n5
    n10 --> n6
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_task_postponement.md"
    click n3 "../modules/task_postponement_service.md"
    click n4 "../modules/task_reactivation_service.md"
    click n5 "../modules/task_replacement_service.md"
    click n6 "../modules/time.md"
    click n7 "../modules/test_task_postponement_migration.md"
    click n8 "../modules/test_task_postponement.md"
    click n9 "../modules/test_task_reactivation.md"
    click n10 "../modules/test_task_supersession.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [task_postponement_service](../modules/task_postponement_service.md) |
| Inbound | [task_reactivation_service](../modules/task_reactivation_service.md) |
| Inbound | [task_replacement_service](../modules/task_replacement_service.md) |
| Inbound | [test_task_postponement_migration](../modules/test_task_postponement_migration.md) |
| Inbound | [test_task_postponement](../modules/test_task_postponement.md) |
| Inbound | [test_task_reactivation](../modules/test_task_reactivation.md) |
| Inbound | [test_task_supersession](../modules/test_task_supersession.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskPostponement](../entities/TaskPostponement.md) | 18 | `Base` | One postponement of one task, kept after reactivation as its history. |
| [TaskReactivationRequirement](../entities/TaskReactivationRequirement.md) | 66 | `Base` | One condition a postponement waits for. |
