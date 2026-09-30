# task_brief Module

**Path:** `backend/app/models/task_brief.py`

## Description

Append-only brief, progress and ordinary review history.

These records describe task collaboration. Autonomous work-package verification
continues to require its own trusted evidence and fenced verifier protocol.

Brief revisions, criterion progress and review verdicts are append-only records. Original task IDs preserve historical identity when a task is removed; current links may become null. These collaboration records do not replace the trusted autonomous work-package verification protocol.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `ForeignKey`, `Integer`, `JSON`, `String`, `Text`, `UniqueConstraint`, `event` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/task_brief.py"]
    n3["backend/app/routers/task_domain.py"]
    n4["backend/app/services/task_brief_service.py"]
    n5["backend/app/services/task_recovery_service.py"]
    n6["backend/app/utils/time.py"]
    n7["backend/tests/test_task_domain.py"]
    n8["backend/tests/test_task_domain_integrity.py"]
    n1 --> n2
    n2 --> n0
    n2 --> n6
    n3 --> n0
    n3 --> n2
    n3 --> n4
    n4 --> n2
    n5 --> n2
    n7 --> n2
    n7 --> n4
    n7 --> n6
    n8 --> n2
    n8 --> n4
    n8 --> n7
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_task_brief.md"
    click n3 "../modules/routers_task_domain.md"
    click n4 "../modules/task_brief_service.md"
    click n5 "../modules/task_recovery_service.md"
    click n6 "../modules/time.md"
    click n7 "../modules/test_task_domain.md"
    click n8 "../modules/test_task_domain_integrity.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [routers_task_domain](../modules/routers_task_domain.md) |
| Inbound | [task_brief_service](../modules/task_brief_service.md) |
| Inbound | [task_recovery_service](../modules/task_recovery_service.md) |
| Inbound | [test_task_domain](../modules/test_task_domain.md) |
| Inbound | [test_task_domain_integrity](../modules/test_task_domain_integrity.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskBriefRevision](../entities/TaskBriefRevision.md) | 16 | `Base` | — |
| [TaskProgressRecord](../entities/TaskProgressRecord.md) | 30 | `Base` | — |
| [TaskReviewRecord](../entities/TaskReviewRecord.md) | 44 | `Base` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_immutable_history` | `(*_args)` | — | — |