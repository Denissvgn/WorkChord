# project_service Module

**Path:** `backend/app/services/project_service.py`

## Description

Project metadata pages have ascending IDs and a carried initial upper bound, so later inserts cannot prolong the selector walk. Each page remains permission-scoped. Portfolio/task metrics remain complete SQL aggregates rather than sums of visible rows.

Project service with CRUD and summary logic.

Creation persists the validated declared working timezone, retaining the compatible UTC default. Subsequent metadata updates preserve the stored zone unless the caller explicitly changes it; local work and metric dates consume that declared project zone rather than inferring historical location.

Deletion preflights management authority, task and dependency constraints, and queued or active execution references. Unsafe execution scope prevents removal before task detachment; a successful removal retains attributable audit and outbox history without reusing the project's recording identity.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `atomic_command`, `lock_planning`, `commit_or_flush`, `schedule_input_command` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Initiative`, `Project`, `ProjectMilestone`, `ProjectMilestoneStatus`, `ProjectStatus`, `ProjectUpdateEntry` |
| `app.models.task` | `Task`, `TaskDependency`, `TaskStatus` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile` |
| `app.query_limits` | `CollectionLimitExceededError`, `MAX_BOUNDED_LIST_ITEMS`, `MAX_PROJECT_LIST_ITEMS`, `MAX_PROJECT_TREE_TASKS` |
| `app.schemas.project` | `InitiativeCreate`, `InitiativeUpdate`, `ProjectCreate`, `ProjectMilestoneCreateRequest`, `ProjectMilestoneSummary`, `ProjectMilestoneTaskGroup`, `ProjectMilestoneUpdate`, `ProjectPortfolioSummary`, `ProjectSummary`, `STALE_PROJECT_UPDATE_DAYS`, `ProjectTargetDateRisk`, `ProjectUpdate`, `ProjectUpdateEntryCreate`, `ProjectUpdateEntryResponse`, `ProjectUpdateFreshness` |
| `app.schemas.team` | `TeamMemberOptionResponse`, `TeamMemberProfileCompact` |
| `app.services.outbound_webhook_service` | `emit_outbound_webhook_event` |
| `app.services.request_source_service` | `RequestSourceService` |
| `app.sql_semantics` | `portable_case_insensitive_equal` |
| `app.utils.time` | `as_utc`, `utc_now` |
| `datetime` | `date`, `datetime` |
| `sqlalchemy` | `Select`, `case`, `exists`, `func`, `select`, `update` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `sqlalchemy.orm` | `aliased`, `selectinload` |
| `typing` | `Optional`, `Sequence` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/project_service.py"]
    n2["scripts"]
    n0 --> n1
    n1 --> n0
    n2 --> n1
    click n1 "../modules/project_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (11) |
| Inbound | `scripts` (1) |
| Outbound | `backend` (12) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 24 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [ProjectService](../entities/ProjectService.md) | 53 | — | Service for project CRUD, linked task retrieval, and summary metrics. |
