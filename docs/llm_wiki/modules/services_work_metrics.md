# work_metrics Module

**Path:** `backend/app/services/work_metrics.py`

## Description

Canonical leaf work, acceptance and distinct calendar-based schedule signals.

Python projections and the recursive SQL aggregate distinguish required/optional/deferred leaves, implemented work, current accepted work, unknown historic acceptance, late start, overdue open delivery and forecast overflow. Working dates use project or calendar zones. Structural parents do not inflate delivery denominators, and unresolved hierarchy cannot be silently treated as complete input.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `_scope_conditions` |
| `app.commands` | `HierarchyScopeError` |
| `app.models.calendar` | `Calendar` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task`, `Task`, `TaskDependency` |
| `app.query_limits` | `CollectionLimitExceededError`, `MAX_PROJECT_TREE_TASKS` |
| `app.utils.time` | `as_utc`, `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `select`, `select`, `case`, `func`, `or_`, `and_`, `false`, `literal` |
| `zoneinfo` | `ZoneInfo` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/work_metrics.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/services_work_metrics.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (4) |
| Outbound | `backend` (8) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `working_today` | `(timezone = 'UTC', now: datetime \| None = None)` | — | — |
| `task_signals` | `(task, *, iteration_end = None, project_target = None, timezone = 'UTC', now = None, composite = False)` | — | — |
| `leaf_metrics` | `(tasks, *, iteration_end = None, project_target = None, timezone = 'UTC', now = None)` | — | Use a complete scoped task set; parents never contribute additional delivered work. |
| `scoped_metric_tasks` | *(async)* `(db, *, project_id = None, iteration_id = None)` | — | — |
| `aggregate_metrics` | *(async)* `(db, *, project_id = None, iteration_id = None, project_ids = None, group_by = None, task_ids = None, zone_map = None)` | — | Aggregate all authorized leaves in SQL, including inherited scheduling facets. |
