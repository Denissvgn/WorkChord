# iteration_service Module

**Path:** `backend/app/services/iteration_service.py`

## Description

Iteration metadata has an additive bounded ID-page contract with an initial upper bound. Existing newest-first small lists and date/ID pages remain compatible. Clients may restore display ordering after a finite authorized selector read.

Iteration service with business logic.

Calendar reassignment refreshes nominal workday and derived effort-day values under the existing planning transaction and version reservations. Canonical hours, unknown or zero estimates, estimate provenance and actual execution records are preserved.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `commit_or_flush`, `schedule_input_command` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project`, `ProjectMilestone` |
| `app.models.task` | `Task`, `TaskStatus` |
| `app.models.team_member` | `TeamMember` |
| `app.query_limits` | `CollectionLimitExceededError`, `MAX_ITERATION_LIST_ITEMS`, `MAX_ITERATION_TREE_TASKS` |
| `app.schemas.iteration` | `IterationCreate`, `IterationPlanningReadinessSummary`, `IterationProjectSummary`, `IterationResponse`, `IterationSeriesCreate`, `IterationSummary`, `IterationUpdate` |
| `app.services.calendar_service` | `CalendarService` |
| `dataclasses` | `dataclass` |
| `datetime` | `date`, `timedelta` |
| `re` | `re` |
| `sqlalchemy` | `and_`, `case`, `exists`, `func`, `or_`, `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `sqlalchemy.orm` | `aliased`, `selectinload` |
| `typing` | `Optional`, `Sequence` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/iteration_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/iteration_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (15) |
| Outbound | `backend` (8) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 23 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [IterationSeriesItem](../entities/IterationSeriesItem.md) | 37 | — | Computed iteration row for a series create request. |
| [IterationService](../entities/IterationService.md) | 44 | — | Service for iteration operations. |