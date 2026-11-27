# DeliveryDependency

**Location:** `backend/app/models/delivery_dependency.py:9`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_delivery_dependency](../modules/models_delivery_dependency.md)

## Description

A dependent task points to exactly one prerequisite task or milestone. Targets are protected from implicit deletion; local schedule edges remain a separate relation.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True)` | — |
| `task_id` | `Mapped[int]` | `mapped_column(ForeignKey('tasks.id', ondelete='CASCADE'), index=True)` | — |
| `prerequisite_task_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('tasks.id', ondelete='RESTRICT'), index=True)` | — |
| `prerequisite_milestone_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('project_milestones.id', ondelete='RESTRICT'), index=True)` | — |
| `target_branch` | `Mapped[str \| None]` | `mapped_column(String(255))` | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DeliveryDependency (backend/app/models/delivery_dependency.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["backend/app/services/agent_service.py"]
    n4["backend/app/services/backlog_snapshot_service.py"]
    n5["DeliveryDependencyService.add (backend/app/services/delivery_dependency_service.py)"]
    n6["backend/app/services/project_service.py"]
    n7["backend/app/services/snapshot_service.py"]
    n8["TaskReplacementService._move_dependents (backend/app/services/task_replacement_service.py)"]
    n9["backend/app/services/task_service.py"]
    n10["_source_artifacts (backend/tests/database_migration/test_postgresql_transfer.py)"]
    n11["backend/tests/migrations/test_delivery_target_branch_migration.py"]
    n12["backend/tests/test_delivery_dependencies.py"]
    n13["backend/tests/test_delivery_prerequisite_tools.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    n13 --> n0
    click n0 "../modules/models_delivery_dependency.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/agent_service.md"
    click n4 "../modules/backlog_snapshot_service.md"
    click n5 "../modules/delivery_dependency_service.md"
    click n6 "../modules/project_service.md"
    click n7 "../modules/snapshot_service.md"
    click n8 "../modules/task_replacement_service.md"
    click n9 "../modules/task_service.md"
    click n10 "../modules/test_postgresql_transfer.md"
    click n11 "../modules/test_delivery_target_branch_migration.md"
    click n12 "../modules/test_delivery_dependencies.md"
    click n13 "../modules/test_delivery_prerequisite_tools.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_delivery_dependency](../modules/models_delivery_dependency.md) | 0 | `id`, `prerequisite_milestone_id`, `prerequisite_task_id`, `target_branch`, `task_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `agent_service` | import | [agent_service](../modules/agent_service.md) | — |
| `backlog_snapshot_service` | import | [backlog_snapshot_service](../modules/backlog_snapshot_service.md) | — |
| `DeliveryDependencyService.add` | call | [delivery_dependency_service](../modules/delivery_dependency_service.md) | 1 |
| `project_service` | import | [project_service](../modules/project_service.md) | — |
| `snapshot_service` | import | [snapshot_service](../modules/snapshot_service.md) | — |
| `TaskReplacementService._move_dependents` | call | [task_replacement_service](../modules/task_replacement_service.md) | 1 |
| `task_service` | import | [task_service](../modules/task_service.md) | — |
| `_source_artifacts` | call | [test_postgresql_transfer](../modules/test_postgresql_transfer.md) | 2 |
| `test_delivery_target_branch_migration` | import | [test_delivery_target_branch_migration](../modules/test_delivery_target_branch_migration.md) | — |
| `test_delivery_dependencies` | import | [test_delivery_dependencies](../modules/test_delivery_dependencies.md) | — |
| `test_delivery_prerequisite_tools` | import | [test_delivery_prerequisite_tools](../modules/test_delivery_prerequisite_tools.md) | — |

> References: showing 12 of 21 logical references; 9 omitted by the 12-row generated summary limit.
