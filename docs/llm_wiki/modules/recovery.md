# recovery Module

**Path:** `backend/app/models/recovery.py`

## Description

Transactional application recovery points and explicit schedule commitments.

Application snapshots and their legacy provenance inventory live in the database. Schedule baseline history records explicit commitments separately from mutable forecasts and actual UTC events. These records support scoped application recovery and are not a substitute for a complete database backup.

The task deletion hook writes the highest observed task version to an independent table in the same ORM transaction, including cascaded children and removals during recovery. Rollback removes an uncommitted fence. A surviving fence protects later reuse of the task ID; the upgrade does not invent records for historical deletions.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.models.task` | `Task`, `Task` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `date`, `datetime` |
| `sqlalchemy` | `ForeignKey`, `Integer`, `JSON`, `String`, `Text`, `UniqueConstraint`, `CheckConstraint`, `Date`, `case`, `event`, `select` |
| `sqlalchemy.dialects.postgresql` | `insert` |
| `sqlalchemy.dialects.sqlite` | `insert` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/recovery.py"]
    n3["backend/app/models/task.py"]
    n4["backend/app/services/backlog_snapshot_service.py"]
    n5["backend/app/services/snapshot_service.py"]
    n6["backend/app/services/task_recovery_service.py"]
    n7["backend/app/utils/time.py"]
    n8["backend/tests/test_identity_lifecycle.py"]
    n9["backend/tests/test_managed_authority.py"]
    n10["backend/tests/test_task_domain_integrity.py"]
    n11["backend/tests/test_work_correctness.py"]
    n1 --> n2
    n1 --> n3
    n2 --> n0
    n2 --> n3
    n2 --> n7
    n3 --> n0
    n3 --> n7
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n4 --> n7
    n5 --> n2
    n5 --> n7
    n6 --> n2
    n8 --> n2
    n8 --> n3
    n8 --> n5
    n8 --> n7
    n8 --> n9
    n9 --> n2
    n9 --> n3
    n9 --> n7
    n10 --> n2
    n10 --> n3
    n10 --> n4
    n10 --> n5
    n11 --> n2
    n11 --> n3
    n11 --> n5
    n11 --> n7
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/recovery.md"
    click n3 "../modules/models_task.md"
    click n4 "../modules/backlog_snapshot_service.md"
    click n5 "../modules/snapshot_service.md"
    click n6 "../modules/task_recovery_service.md"
    click n7 "../modules/time.md"
    click n8 "../modules/test_identity_lifecycle.md"
    click n9 "../modules/test_managed_authority.md"
    click n10 "../modules/test_task_domain_integrity.md"
    click n11 "../modules/test_work_correctness.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [backlog_snapshot_service](../modules/backlog_snapshot_service.md) |
| Inbound | [snapshot_service](../modules/snapshot_service.md) |
| Inbound | [task_recovery_service](../modules/task_recovery_service.md) |
| Inbound | [test_identity_lifecycle](../modules/test_identity_lifecycle.md) |
| Inbound | [test_managed_authority](../modules/test_managed_authority.md) |
| Inbound | [test_task_domain_integrity](../modules/test_task_domain_integrity.md) |
| Inbound | [test_work_correctness](../modules/test_work_correctness.md) |
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
| [ApplicationSnapshot](../entities/ApplicationSnapshot.md) | 12 | `Base` | — |
| [LegacySnapshotImport](../entities/LegacySnapshotImport.md) | 30 | `Base` | — |
| [TaskScheduleBaseline](../entities/TaskScheduleBaseline.md) | 40 | `Base` | — |
| [TaskDeletionFence](../entities/TaskDeletionFence.md) | 54 | `Base` | Retain the highest deleted task version independently of task lifetime. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `record_task_deletion_fence` | `(_mapper, connection, task)` | — | Join the authorized ORM deletion transaction, including cascaded children. |