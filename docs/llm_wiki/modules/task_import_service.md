# task_import_service Module

**Path:** `backend/app/services/task_import_service.py`

## Description

Task text import, export, and triage intake workflows.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `commit_or_flush` |
| `app.models.task` | `Task` |
| `app.models.triage` | `TriageItem`, `TriageItemStatus` |
| `app.schemas.task` | `TaskImportDestination` |
| `app.services.snapshot_service` | `SnapshotService` |
| `app.services.task_service` | `TaskService` |
| `json` | `json` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Optional`, `TYPE_CHECKING` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/commands.py"]
    n1["backend/app/models/task.py"]
    n2["backend/app/models/triage.py"]
    n3["backend/app/schemas/task.py"]
    n4["backend/app/services/snapshot_service.py"]
    n5["backend/app/services/task_import_service.py"]
    n6["backend/app/services/task_service.py"]
    n0 --> n1
    n0 --> n4
    n0 --> n6
    n2 --> n1
    n4 --> n0
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n5 --> n6
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n4
    click n0 "../modules/commands.md"
    click n1 "../modules/models_task.md"
    click n2 "../modules/models_triage.md"
    click n3 "../modules/schemas_task.md"
    click n4 "../modules/snapshot_service.md"
    click n5 "../modules/task_import_service.md"
    click n6 "../modules/task_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [commands](../modules/commands.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [models_triage](../modules/models_triage.md) |
| Outbound | [schemas_task](../modules/schemas_task.md) |
| Outbound | [snapshot_service](../modules/snapshot_service.md) |
| Outbound | [task_service](../modules/task_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskImportService](../entities/TaskImportService.md) | 19 | — | Own task text parsing, assignee resolution, and import persistence. |
