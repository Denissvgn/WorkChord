# TaskProgressRecord

**Location:** `backend/app/models/task_brief.py:30`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_task_brief](../modules/models_task_brief.md)

## Description

_Auto-generated from `TaskProgressRecord` in `backend/app/models/task_brief.py`._

Immutable worker-reported criterion states, evidence and artifact links, bound to the brief and artifact revision. Reporting progress grants no acceptance authority.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True)` | — |
| `task_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('tasks.id', ondelete='SET NULL'), index=True)` | — |
| `original_task_id` | `Mapped[int]` | `mapped_column(Integer, index=True)` | — |
| `task_version` | `Mapped[int]` | `mapped_column(Integer)` | — |
| `brief_revision` | `Mapped[int]` | `mapped_column(Integer)` | — |
| `artifact_revision` | `Mapped[int]` | `mapped_column(Integer)` | — |
| `principal_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('principals.id', ondelete='RESTRICT'))` | — |
| `payload` | `Mapped[dict]` | `mapped_column(JSON)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskProgressRecord (backend/app/models/task_brief.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["backend/app/routers/task_domain.py"]
    n4["TaskBriefService.write_progress (backend/app/services/task_brief_service.py)"]
    n5["backend/app/services/task_recovery_service.py"]
    n6["backend/tests/test_task_domain.py"]
    n7["backend/tests/test_task_domain_integrity.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/models_task_brief.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/routers_task_domain.md"
    click n4 "../modules/task_brief_service.md"
    click n5 "../modules/task_recovery_service.md"
    click n6 "../modules/test_task_domain.md"
    click n7 "../modules/test_task_domain_integrity.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_task_brief](../modules/models_task_brief.md) | 0 | `artifact_revision`, `brief_revision`, `created_at`, `id`, `original_task_id`, `payload`, `principal_id`, `task_id`, `task_version` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `task_domain` | import | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `TaskBriefService.write_progress` | call | [task_brief_service](../modules/task_brief_service.md) | 1 |
| `task_recovery_service` | import | [task_recovery_service](../modules/task_recovery_service.md) | — |
| `test_task_domain` | import | [test_task_domain](../modules/test_task_domain.md) | — |
| `test_task_domain_integrity` | import | [test_task_domain_integrity](../modules/test_task_domain_integrity.md) | — |
