# snapshot_service Module

**Path:** `backend/app/services/snapshot_service.py`

## Description

Snapshot service for iteration state backups.

## Imports

| Source | Symbols |
|--------|---------|
| `app.services.iteration_service` | `IterationService` |
| `app.services.team_service` | `TeamService` |
| `app.utils.time` | `utc_now` |
| `datetime` | `timedelta` |
| `json` | `json` |
| `pathlib` | `Path` |
| `re` | `re` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/routers/snapshots.py"]
    n1["backend/app/services/iteration_service.py"]
    n2["backend/app/services/plan_share_service.py"]
    n3["backend/app/services/snapshot_service.py"]
    n4["backend/app/services/task_import_service.py"]
    n5["backend/app/services/task_service.py"]
    n6["backend/app/services/team_service.py"]
    n7["backend/app/utils/time.py"]
    n0 --> n1
    n0 --> n3
    n0 --> n5
    n0 --> n6
    n2 --> n3
    n2 --> n7
    n3 --> n1
    n3 --> n6
    n3 --> n7
    n4 --> n3
    n4 --> n5
    n5 --> n3
    click n0 "../modules/snapshots.md"
    click n1 "../modules/iteration_service.md"
    click n2 "../modules/plan_share_service.md"
    click n3 "../modules/snapshot_service.md"
    click n4 "../modules/task_import_service.md"
    click n5 "../modules/task_service.md"
    click n6 "../modules/team_service.md"
    click n7 "../modules/time.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [snapshots](../modules/snapshots.md) |
| Inbound | [plan_share_service](../modules/plan_share_service.md) |
| Inbound | [task_import_service](../modules/task_import_service.md) |
| Inbound | [task_service](../modules/task_service.md) |
| Outbound | [iteration_service](../modules/iteration_service.md) |
| Outbound | [team_service](../modules/team_service.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [SnapshotPathError](../entities/SnapshotPathError.md) | 22 | `ValueError` | Raised when a snapshot name cannot be safely resolved inside its iteration directory. |
| [SnapshotService](../entities/SnapshotService.md) | 26 | — | Service for creating and managing iteration snapshots. |
