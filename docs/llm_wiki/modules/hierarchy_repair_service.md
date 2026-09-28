# hierarchy_repair_service Module

**Path:** `backend/app/services/hierarchy_repair_service.py`

## Description

Operator-scoped, bounded hierarchy diagnosis and version-checked deterministic repair.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `require_operator` |
| `app.commands` | `atomic_command`, `lock_iterations` |
| `app.models.task` | `Task` |
| `app.services.snapshot_service` | `SnapshotService` |
| `app.services.task_service` | `TaskService` |
| `app.services.task_status_service` | `TaskStatusService` |
| `app.services.work_metrics` | `scoped_metric_tasks`, `task_signals` |
| `sqlalchemy` | `select` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/commands.py"]
    n2["backend/app/models/task.py"]
    n3["backend/app/routers/snapshots.py"]
    n4["backend/app/services/hierarchy_repair_service.py"]
    n5["backend/app/services/snapshot_service.py"]
    n6["backend/app/services/task_service.py"]
    n7["backend/app/services/task_status_service.py"]
    n8["backend/app/services/work_metrics.py"]
    n9["backend/tests/test_work_correctness.py"]
    n0 --> n2
    n1 --> n0
    n1 --> n2
    n1 --> n5
    n1 --> n6
    n3 --> n1
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n5 --> n1
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n5
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n6
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n9 --> n0
    n9 --> n1
    n9 --> n2
    n9 --> n4
    n9 --> n5
    n9 --> n6
    n9 --> n8
    click n0 "../modules/authority.md"
    click n1 "../modules/commands.md"
    click n2 "../modules/models_task.md"
    click n3 "../modules/snapshots.md"
    click n4 "../modules/hierarchy_repair_service.md"
    click n5 "../modules/snapshot_service.md"
    click n6 "../modules/task_service.md"
    click n7 "../modules/task_status_service.md"
    click n8 "../modules/services_work_metrics.md"
    click n9 "../modules/test_work_correctness.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [snapshots](../modules/snapshots.md) |
| Inbound | [test_work_correctness](../modules/test_work_correctness.md) |
| Outbound | [authority](../modules/authority.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [snapshot_service](../modules/snapshot_service.md) |
| Outbound | [task_service](../modules/task_service.md) |
| Outbound | [task_status_service](../modules/task_status_service.md) |
| Outbound | [services_work_metrics](../modules/services_work_metrics.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [HierarchyRepairService](../entities/HierarchyRepairService.md) | 14 | — | — |
