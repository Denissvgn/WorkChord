# snapshot_service Module

**Path:** `backend/app/services/snapshot_service.py`

## Description

Snapshot service for iteration state backups.

Stores bounded, checksummed pre-command points transactionally in the database; preview and failed commands cannot publish or evict them. Captured project scopes gate payload reads. Restore preserves supported IDs, recovers captured iteration dates and absences, records baseline restoration, and invalidates current acceptance. Ambiguous legacy files remain quarantined provenance records. Global configuration and external side effects require separate recovery.

Scheduled and backlog restoration share a version allocator under the owning scope lock. It advances above the saved version, live task, retained history and durable deletion fence. Current progress and acceptance are cleared; immutable history survives. A deleted task without a reliable deletion fence returns snapshot_version_history_unknown (409), requiring recovery from a complete matching database backup.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `atomic_command`, `current_command`, `lock_iterations` |
| `app.config` | `get_settings` |
| `app.models.recovery` | `ApplicationSnapshot`, `LegacySnapshotImport` |
| `app.services.iteration_service` | `IterationService` |
| `app.services.team_service` | `TeamService` |
| `app.utils.time` | `utc_now` |
| `datetime` | `datetime`, `timedelta` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `pathlib` | `Path` |
| `re` | `re` |
| `sqlalchemy` | `select`, `delete` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/snapshot_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/snapshot_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (12) |
| Outbound | `backend` (6) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 17 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [SnapshotPathError](../entities/SnapshotPathError.md) | 27 | `ValueError` | Raised when a snapshot name cannot be safely resolved inside its iteration directory. |
| [SnapshotService](../entities/SnapshotService.md) | 31 | — | Service for creating and managing iteration snapshots. |