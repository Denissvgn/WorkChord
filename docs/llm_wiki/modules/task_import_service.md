# task_import_service Module

**Path:** `backend/app/services/task_import_service.py`

## Description

Task and triage text imports share one authorized aggregate reservation, recovery point and transaction. Observed revisions are accepted additively for compatibility, with strict requirements controlled by server policy. Direct collaborator calls use the same transaction and revision guard.

Task text import, export, and triage intake workflows.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `require_project` |
| `app.commands` | `atomic_command`, `commit_or_flush`, `lock_iterations` |
| `app.models.task` | `Task` |
| `app.models.triage` | `TriageItem`, `TriageItemStatus` |
| `app.schemas.task` | `TaskImportDestination` |
| `app.services.snapshot_service` | `SnapshotService` |
| `app.services.task_domain_service` | `nominal_day_hours` |
| `app.services.task_service` | `TaskService` |
| `json` | `json` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Optional`, `TYPE_CHECKING` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/commands.py"]
    n2["backend/app/models/task.py"]
    n3["backend/app/models/triage.py"]
    n4["backend/app/schemas/task.py"]
    n5["backend/app/services/snapshot_service.py"]
    n6["backend/app/services/task_domain_service.py"]
    n7["backend/app/services/task_import_service.py"]
    n8["backend/app/services/task_service.py"]
    n0 --> n2
    n1 --> n0
    n1 --> n2
    n1 --> n5
    n1 --> n8
    n3 --> n2
    n5 --> n1
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n5
    n7 --> n6
    n7 --> n8
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n3
    n8 --> n4
    n8 --> n5
    click n0 "../modules/authority.md"
    click n1 "../modules/commands.md"
    click n2 "../modules/models_task.md"
    click n3 "../modules/models_triage.md"
    click n4 "../modules/schemas_task.md"
    click n5 "../modules/snapshot_service.md"
    click n6 "../modules/task_domain_service.md"
    click n7 "../modules/task_import_service.md"
    click n8 "../modules/task_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [authority](../modules/authority.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [models_triage](../modules/models_triage.md) |
| Outbound | [schemas_task](../modules/schemas_task.md) |
| Outbound | [snapshot_service](../modules/snapshot_service.md) |
| Outbound | [task_domain_service](../modules/task_domain_service.md) |
| Outbound | [task_service](../modules/task_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskImportService](../entities/TaskImportService.md) | 21 | — | Own task text parsing, assignee resolution, and import persistence. |
