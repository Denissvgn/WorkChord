# recovery Module

**Path:** `backend/app/models/recovery.py`

## Description

Transactional application recovery points and explicit schedule commitments.

Application snapshots and their legacy provenance inventory live in the database. Schedule baseline history records explicit commitments separately from mutable forecasts and actual UTC events. These records support scoped application recovery and are not a substitute for a complete database backup.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `date`, `datetime` |
| `sqlalchemy` | `ForeignKey`, `Integer`, `JSON`, `String`, `Text`, `UniqueConstraint`, `Date` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/recovery.py"]
    n3["backend/app/services/snapshot_service.py"]
    n4["backend/app/utils/time.py"]
    n5["backend/tests/test_identity_lifecycle.py"]
    n6["backend/tests/test_managed_authority.py"]
    n7["backend/tests/test_work_correctness.py"]
    n1 --> n2
    n2 --> n0
    n2 --> n4
    n3 --> n2
    n3 --> n4
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n5 --> n6
    n6 --> n2
    n6 --> n4
    n7 --> n2
    n7 --> n3
    n7 --> n4
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/recovery.md"
    click n3 "../modules/snapshot_service.md"
    click n4 "../modules/time.md"
    click n5 "../modules/test_identity_lifecycle.md"
    click n6 "../modules/test_managed_authority.md"
    click n7 "../modules/test_work_correctness.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [snapshot_service](../modules/snapshot_service.md) |
| Inbound | [test_identity_lifecycle](../modules/test_identity_lifecycle.md) |
| Inbound | [test_managed_authority](../modules/test_managed_authority.md) |
| Inbound | [test_work_correctness](../modules/test_work_correctness.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [ApplicationSnapshot](../entities/ApplicationSnapshot.md) | 12 | `Base` | — |
| [LegacySnapshotImport](../entities/LegacySnapshotImport.md) | 27 | `Base` | — |
| [TaskScheduleBaseline](../entities/TaskScheduleBaseline.md) | 37 | `Base` | — |
