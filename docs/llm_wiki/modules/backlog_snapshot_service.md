# backlog_snapshot_service Module

**Path:** `backend/app/services/backlog_snapshot_service.py`

## Description

Restores project backlog identities under the shared planning and project locks. Incoming delivery references require explicit resolution before target removal. Retained discussion follows original task identity, while current execution evidence and acceptance are cleared and downstream delivery context is reconciled.

Project backlog snapshots share the complete person lifetime capture and preflight boundary. A scoped manager can recover another eligible project member while private profile queries remain scoped. Missing or replaced provenance rejects before writing the pre-restore point.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `AuthorityError`, `internal_authority`, `require_project` |
| `app.commands` | `atomic_command`, `current_command`, `lock_backlog_project` |
| `app.config` | `get_settings` |
| `app.models.recovery` | `ApplicationSnapshot` |
| `app.models.task` | `Task`, `TaskDependency` |
| `app.services.snapshot_service` | `SnapshotService` |
| `app.services.task_service` | `TaskService` |
| `app.utils.time` | `utc_now` |
| `datetime` | `date`, `datetime` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `sqlalchemy` | `delete`, `or_`, `select` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/backlog_snapshot_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/backlog_snapshot_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (7) |
| Outbound | `backend` (8) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 15 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [BacklogSnapshotService](../entities/BacklogSnapshotService.md) | 19 | — | — |