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
| `app.services.task_brief_service` | `clear_execution_evidence`, `clear_execution_evidence`, `clear_execution_evidence` |
| `app.services.task_service` | `TaskService`, `TaskService`, `TaskService`, `TaskService` |
| `collections` | `defaultdict`, `deque` |
| `sqlalchemy` | `or_`, `select` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/delivery_dependency_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/delivery_dependency_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (14) |
| Outbound | `backend` (7) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 18 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [DeliveryDependencyService](../entities/DeliveryDependencyService.md) | 14 | — | — |