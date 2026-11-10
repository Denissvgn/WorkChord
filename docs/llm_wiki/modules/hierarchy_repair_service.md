# hierarchy_repair_service Module

**Path:** `backend/app/services/hierarchy_repair_service.py`

## Description

Operator-scoped, bounded hierarchy diagnosis and version-checked deterministic repair.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `require_operator` |
| `app.commands` | `atomic_command`, `lock_iterations`, `AggregateVersionConflict` |
| `app.models.iteration` | `Iteration` |
| `app.models.task` | `Task` |
| `app.services.snapshot_service` | `SnapshotService` |
| `app.services.task_service` | `TaskService`, `TaskVersionConflictError` |
| `app.services.task_status_service` | `TaskStatusService` |
| `app.services.work_metrics` | `effective_work_flags`, `scoped_metric_tasks`, `task_signals` |
| `sqlalchemy` | `select` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/commands.py"]
    n2["backend/app/models/iteration.py"]
    n3["backend/app/models/task.py"]
    n4["backend/app/routers/snapshots.py"]
    n5["backend/app/services/hierarchy_repair_service.py"]
    n6["backend/app/services/snapshot_service.py"]
    n7["backend/app/services/task_service.py"]
    n8["backend/app/services/task_status_service.py"]
    n9["backend/app/services/work_metrics.py"]
    n10["backend/tests/test_work_correctness.py"]
    n0 --> n3
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n6
    n1 --> n7
    n2 --> n3
    n3 --> n2
    n4 --> n1
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n6
    n5 --> n7
    n5 --> n8
    n5 --> n9
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n7
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n6
    n7 --> n8
    n7 --> n9
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n3
    n8 --> n6
    n8 --> n7
    n8 --> n9
    n9 --> n0
    n9 --> n1
    n9 --> n2
    n9 --> n3
    n10 --> n0
    n10 --> n1
    n10 --> n2
    n10 --> n3
    n10 --> n5
    n10 --> n6
    n10 --> n7
    n10 --> n9
    click n0 "../modules/authority.md"
    click n1 "../modules/commands.md"
    click n2 "../modules/models_iteration.md"
    click n3 "../modules/models_task.md"
    click n4 "../modules/snapshots.md"
    click n5 "../modules/hierarchy_repair_service.md"
    click n6 "../modules/snapshot_service.md"
    click n7 "../modules/task_service.md"
    click n8 "../modules/task_status_service.md"
    click n9 "../modules/services_work_metrics.md"
    click n10 "../modules/test_work_correctness.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [snapshots](../modules/snapshots.md) |
| Inbound | [test_work_correctness](../modules/test_work_correctness.md) |
| Outbound | [authority](../modules/authority.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [models_iteration](../modules/models_iteration.md) |
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
