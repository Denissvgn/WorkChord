# backlog_snapshot_service Module

**Path:** `backend/app/services/backlog_snapshot_service.py`

## Description

Project backlog recovery using the shared transactional snapshot store.

Project backlog recovery uses the shared database snapshot store and the command transaction. Captures are bounded, checksummed and retained per project. Restore checks the complete current task-version map, preserves IDs and immutable brief history, and clears current acceptance/progress. Project authority and dependency scope remain validated.

Scheduled and backlog restoration share a version allocator under the owning scope lock. It advances above the saved version, live task, retained history and durable deletion fence. Current progress and acceptance are cleared; immutable history survives. A deleted task without a reliable deletion fence returns snapshot_version_history_unknown (409), requiring recovery from a complete matching database backup.

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
    n0["backend/app/authority.py"]
    n1["backend/app/commands.py"]
    n2["backend/app/config.py"]
    n3["backend/app/models/recovery.py"]
    n4["backend/app/models/task.py"]
    n5["backend/app/routers/task_domain.py"]
    n6["backend/app/services/backlog_snapshot_service.py"]
    n7["backend/app/services/snapshot_service.py"]
    n8["backend/app/services/task_service.py"]
    n9["backend/app/utils/time.py"]
    n10["backend/tests/test_task_domain.py"]
    n11["backend/tests/test_task_domain_integrity.py"]
    n0 --> n2
    n0 --> n4
    n1 --> n0
    n1 --> n4
    n1 --> n7
    n1 --> n8
    n3 --> n4
    n3 --> n9
    n4 --> n9
    n5 --> n0
    n5 --> n4
    n5 --> n6
    n5 --> n8
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n7
    n6 --> n8
    n6 --> n9
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n9
    n8 --> n0
    n8 --> n1
    n8 --> n4
    n8 --> n7
    n10 --> n0
    n10 --> n1
    n10 --> n4
    n10 --> n6
    n10 --> n8
    n10 --> n9
    n11 --> n0
    n11 --> n1
    n11 --> n3
    n11 --> n4
    n11 --> n6
    n11 --> n7
    n11 --> n8
    n11 --> n10
    click n0 "../modules/authority.md"
    click n1 "../modules/commands.md"
    click n2 "../modules/config.md"
    click n3 "../modules/recovery.md"
    click n4 "../modules/models_task.md"
    click n5 "../modules/routers_task_domain.md"
    click n6 "../modules/backlog_snapshot_service.md"
    click n7 "../modules/snapshot_service.md"
    click n8 "../modules/task_service.md"
    click n9 "../modules/time.md"
    click n10 "../modules/test_task_domain.md"
    click n11 "../modules/test_task_domain_integrity.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_task_domain](../modules/routers_task_domain.md) |
| Inbound | [test_task_domain](../modules/test_task_domain.md) |
| Inbound | [test_task_domain_integrity](../modules/test_task_domain_integrity.md) |
| Outbound | [authority](../modules/authority.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [recovery](../modules/recovery.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [snapshot_service](../modules/snapshot_service.md) |
| Outbound | [task_service](../modules/task_service.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [BacklogSnapshotService](../entities/BacklogSnapshotService.md) | 19 | — | — |