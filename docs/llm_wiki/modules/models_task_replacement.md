# task_replacement Module

**Path:** `backend/app/models/task_replacement.py`

## Description

An audited disposition that replaces unattributable work with a separate clean task.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `JSON`, `CheckConstraint`, `ForeignKey`, `Index`, `Integer`, `String`, `Text`, `UniqueConstraint` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/task_replacement.py"]
    n3["backend/app/services/delivery_dependency_service.py"]
    n4["backend/app/services/task_replacement_service.py"]
    n5["backend/app/utils/time.py"]
    n6["backend/tests/migrations/test_task_replacement_migration.py"]
    n7["backend/tests/test_github_reconciliation.py"]
    n8["backend/tests/test_replacement_carried_provenance.py"]
    n9["backend/tests/test_task_replacement.py"]
    n1 --> n2
    n2 --> n0
    n2 --> n5
    n3 --> n2
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n6 --> n2
    n7 --> n2
    n8 --> n2
    n8 --> n4
    n8 --> n5
    n8 --> n9
    n9 --> n2
    n9 --> n3
    n9 --> n4
    n9 --> n5
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_task_replacement.md"
    click n3 "../modules/delivery_dependency_service.md"
    click n4 "../modules/task_replacement_service.md"
    click n5 "../modules/time.md"
    click n6 "../modules/test_task_replacement_migration.md"
    click n7 "../modules/test_github_reconciliation.md"
    click n8 "../modules/test_replacement_carried_provenance.md"
    click n9 "../modules/test_task_replacement.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [delivery_dependency_service](../modules/delivery_dependency_service.md) |
| Inbound | [task_replacement_service](../modules/task_replacement_service.md) |
| Inbound | [test_task_replacement_migration](../modules/test_task_replacement_migration.md) |
| Inbound | [test_github_reconciliation](../modules/test_github_reconciliation.md) |
| Inbound | [test_replacement_carried_provenance](../modules/test_replacement_carried_provenance.md) |
| Inbound | [test_task_replacement](../modules/test_task_replacement.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskReplacement](../entities/TaskReplacement.md) | 12 | `Base` | Link an original task to the one task that delivers its work instead. |
