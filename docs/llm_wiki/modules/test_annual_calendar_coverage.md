# test_annual_calendar_coverage Module

**Path:** `backend/tests/test_annual_calendar_coverage.py`

## Description

_Auto-generated from `backend/tests/test_annual_calendar_coverage.py`._

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `Authority`, `AuthorityError` |
| `app.commands` | `PlanningConflict` |
| `app.database` | `get_db` |
| `app.main` | `app` |
| `app.models.agent` | `AgentTaskAssignment` |
| `app.models.capacity` | `ProfileAbsence`, `ProfileAvailability` |
| `app.models.iteration` | `Iteration` |
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile`, `Vacation` |
| `app.schemas.calendar` | `CalendarCreate`, `CalendarUpdate` |
| `app.schemas.iteration` | `IterationUpdate`, `IterationSummary` |
| `app.services.agent_routing_service` | `AgentRoutingService` |
| `app.services.calendar_rules` | `AnnualCalendars`, `YearRules` |
| `app.services.calendar_service` | `CalendarService` |
| `app.services.capacity_service` | `CapacityService`, `PeriodCommitments` |
| `app.services.iteration_service` | `IterationService` |
| `app.services.planning_input_context` | `observe_planning_input` |
| `app.services.scheduler_service` | `SchedulerService` |
| `app.services.snapshot_service` | `SnapshotService` |
| `app.services.team_service` | `TeamService` |
| `datetime` | `date`, `timedelta` |
| `httpx` | `httpx` |
| `pytest` | `pytest` |
| `sqlalchemy.ext.asyncio` | `async_sessionmaker` |
| `tests` | `test_profile_capacity` |
| `types` | `SimpleNamespace` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_annual_calendar_coverage.py"]
    n1 --> n0
    click n1 "../modules/test_annual_calendar_coverage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (21) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 21 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `calendars` | *(async)* `(db)` | — | — |
| `test_explicit_iteration_coverage_is_scoped_and_date_correct` | *(async)* `(db_session)` | — | — |
| `test_capacity_scheduler_and_profile_owner_use_each_selected_day` | *(async)* `(db_session)` | — | — |
| `test_invalid_annual_bindings_and_reverse_dependencies` | *(async)* `(db_session)` | — | — |
| `test_interior_year_and_snapshot_use_the_explicit_owner` | *(async)* `(db_session, monkeypatch)` | — | — |
| `test_replacing_issued_annual_rules_is_scoped_to_the_affected_tasks` | *(async)* `(db_session, actor_factory)` | — | — |
| `test_person_primary_change_preserves_the_ordinary_reservation` | *(async)* `(db_session, actor_factory, include_years)` | `@pytest.mark.parametrize('include_years', [False, True])` | — |
| `test_hidden_person_protects_shared_master_without_leaking_their_identity` | *(async)* `(db_session)` | — | — |
| `test_routing_preserves_single_year_ratios_and_uses_each_annual_nominal` | *(async)* `(db_session)` | — | — |
| `test_repeated_long_commitments_are_indexed_by_owner_and_year` | *(async)* `(db_session, monkeypatch, record_property)` | — | — |
| `test_registered_iteration_summary_retains_its_schema_description` | `()` | — | — |
