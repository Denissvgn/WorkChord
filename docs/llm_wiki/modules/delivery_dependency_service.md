# delivery_dependency_service Module

**Path:** `backend/app/services/delivery_dependency_service.py`

## Description

Owns typed task/milestone delivery prerequisites, distinct from local schedule dependencies. Creation checks both endpoint visibility and global cycles across hierarchy, milestone and dependency edges. Readiness requires current attributed acceptance; inaccessible targets expose only a generic blocker. Changes propagate version and evidence invalidation transactionally, while deletion and project changes require explicit link resolution.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `AuthorityError`, `internal_authority`, `require_project` |
| `app.commands` | `PlanningConflict`, `atomic_command`, `lock_planning` |
| `app.models.delivery_dependency` | `DeliveryDependency` |
| `app.models.project` | `ProjectMilestone` |
| `app.models.task` | `Task`, `TaskDependency` |
| `collections` | `defaultdict`, `deque` |
| `sqlalchemy` | `or_`, `select` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/commands.py"]
    n2["backend/app/models/delivery_dependency.py"]
    n3["backend/app/models/project.py"]
    n4["backend/app/models/task.py"]
    n5["backend/app/routers/delivery_dependencies.py"]
    n6["backend/app/routers/tasks.py"]
    n7["backend/app/services/delivery_dependency_service.py"]
    n8["backend/tests/test_delivery_dependencies.py"]
    n0 --> n4
    n1 --> n0
    n1 --> n3
    n1 --> n4
    n1 --> n7
    n2 --> n3
    n2 --> n4
    n3 --> n4
    n4 --> n3
    n5 --> n7
    n6 --> n1
    n6 --> n4
    n6 --> n7
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n3
    n8 --> n4
    n8 --> n7
    click n0 "../modules/authority.md"
    click n1 "../modules/commands.md"
    click n2 "../modules/delivery_dependency.md"
    click n3 "../modules/models_project.md"
    click n4 "../modules/models_task.md"
    click n5 "../modules/delivery_dependencies.md"
    click n6 "../modules/tasks.md"
    click n7 "../modules/delivery_dependency_service.md"
    click n8 "../modules/test_delivery_dependencies.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [commands](../modules/commands.md) |
| Inbound | [delivery_dependencies](../modules/delivery_dependencies.md) |
| Inbound | [tasks](../modules/tasks.md) |
| Inbound | [test_delivery_dependencies](../modules/test_delivery_dependencies.md) |
| Outbound | [authority](../modules/authority.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [delivery_dependency](../modules/delivery_dependency.md) |
| Outbound | [models_project](../modules/models_project.md) |
| Outbound | [models_task](../modules/models_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [DeliveryDependencyService](../entities/DeliveryDependencyService.md) | 14 | — | — |
