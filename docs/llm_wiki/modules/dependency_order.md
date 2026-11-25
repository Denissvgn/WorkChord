# dependency_order Module

**Path:** `backend/app/services/dependency_order.py`

## Description

Saved dependency order: dependents whose persisted dates start before their prerequisite ends.

The scheduler places a dependent on the day after its predecessor's end date
(``end_date`` is inclusive), so a saved start on or before that end date breaks
the order. Only planned leaf work is judged: started or finished work carries
actual dates, work that is deferred, canceled or inside a deferred branch is
backlog, and a prerequisite that is already resolved, closed or canceled no
longer constrains anything. Edges to work outside the iteration are ignored.

This module only reads. Correcting the dates is a schedule preview followed by
an explicit apply.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.commands` | `PlanningConflict` |
| `app.models.task` | `Task`, `TaskDependency`, `TaskStatus` |
| `app.schemas.iteration` | `InvertedDependency` |
| `app.services.work_metrics` | `included_work_ids` |
| `sqlalchemy` | `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/commands.py"]
    n1["backend/app/models/task.py"]
    n2["backend/app/routers/gantt.py"]
    n3["backend/app/schemas/iteration.py"]
    n4["backend/app/services/dependency_order.py"]
    n5["backend/app/services/iteration_service.py"]
    n6["backend/app/services/work_metrics.py"]
    n0 --> n1
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n4 --> n0
    n4 --> n1
    n4 --> n3
    n4 --> n6
    n5 --> n0
    n5 --> n1
    n5 --> n3
    n5 --> n4
    n5 --> n6
    n6 --> n0
    n6 --> n1
    click n0 "../modules/commands.md"
    click n1 "../modules/models_task.md"
    click n2 "../modules/routers_gantt.md"
    click n3 "../modules/schemas_iteration.md"
    click n4 "../modules/dependency_order.md"
    click n5 "../modules/iteration_service.md"
    click n6 "../modules/services_work_metrics.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_gantt](../modules/routers_gantt.md) |
| Inbound | [iteration_service](../modules/iteration_service.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [schemas_iteration](../modules/schemas_iteration.md) |
| Outbound | [services_work_metrics](../modules/services_work_metrics.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `inverted_saved_dependencies` | *(async)* `(db: AsyncSession, iteration_id: int) -> list[InvertedDependency]` | — | List the dependency pairs of one iteration whose saved dates are inverted. |
