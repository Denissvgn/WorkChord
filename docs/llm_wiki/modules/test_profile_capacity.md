# test_profile_capacity Module

**Path:** `backend/tests/test_profile_capacity.py`

## Description

Shared person capacity, calendar arithmetic and private availability boundaries.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `Authority`, `AuthorityError` |
| `app.commands` | `PlanningConflict`, `command_transaction`, `command_transaction`, `command_transaction`, `command_transaction` |
| `app.database` | `Base` |
| `app.models.calendar` | `Calendar` |
| `app.models.capacity` | `PlanningState`, `ProfileAbsence` |
| `app.models.identity` | `Principal` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task`, `Task`, `Task` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile`, `Vacation` |
| `app.schemas.calendar` | `CalendarCreate` |
| `app.schemas.team` | `VacationCreate`, `VacationUpdate`, `TeamMemberUpdate` |
| `app.services.calendar_service` | `CalendarService`, `CalendarService` |
| `app.services.capacity_service` | `CapacityService`, `day_hours` |
| `app.services.scheduler_service` | `MemberSchedule`, `SchedulerService`, `SchedulerService`, `SchedulerService`, `SchedulerService` |
| `app.services.snapshot_service` | `SnapshotService` |
| `app.services.team_service` | `TeamService` |
| `asyncio` | `asyncio`, `asyncio` |
| `datetime` | `date` |
| `pydantic` | `ValidationError` |
| `pytest` | `pytest` |
| `pytest_asyncio` | `pytest_asyncio` |
| `sqlalchemy` | `select` |
| `sqlalchemy.ext.asyncio` | `async_sessionmaker`, `create_async_engine` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_profile_capacity.py"]
    n1 --> n0
    click n1 "../modules/test_profile_capacity.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (17) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 4 | 2 |

> All 17 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_partial_absence_update_cannot_clear_required_dates` | `()` | — | — |
| `test_created_short_days_apply_once_to_fractional_shared_capacity` | *(async)* `(db_session)` | — | — |
| `db_session` | *(async)* `(request, sqlite_engine)` | `@pytest_asyncio.fixture(params=[pytest.param('sqlite', marks=pytest.mark.sqlite), pytest.param('postgresql', marks=[pytest.mark.postgresql, pytest.mark.allow_network])])` | — |
| `allocation` | *(async)* `(db, *, hours = 6, profile = None)` | — | — |
| `test_capacity_counts_union_of_absences_and_actual_calendar_hours` | *(async)* `(db_session)` | `@pytest.mark.asyncio` | — |
| `test_profile_absence_applies_to_other_allocations` | *(async)* `(db_session)` | `@pytest.mark.asyncio` | — |
| `test_shared_absence_revisions_legacy_adapter_and_stale_write` | *(async)* `(db_session)` | `@pytest.mark.asyncio` | — |
| `test_absence_owner_permission_and_projection_redaction` | *(async)* `(db_session)` | `@pytest.mark.asyncio` | — |
| `test_preview_absence_rolls_back_planning_and_absence` | *(async)* `(db_session)` | `@pytest.mark.asyncio` | — |
| `test_concurrent_absence_edits_have_one_winner` | *(async)* `(db_session)` | `@pytest.mark.asyncio` | — |
| `test_canonical_calendar_and_fractional_capacity_preserve_unknown_work` | *(async)* `(db_session)` | `@pytest.mark.asyncio` | — |
| `test_short_workday_and_overflow_are_reserved_for_the_person` | `()` | — | — |
| `test_schedule_preview_is_pure_and_rejects_changed_shared_inputs` | *(async)* `(db_session)` | `@pytest.mark.asyncio` | — |
| `test_overallocated_person_can_preview_but_cannot_commit` | *(async)* `(db_session)` | `@pytest.mark.asyncio` | — |
| `test_two_planners_cannot_commit_the_same_shared_revision` | *(async)* `(db_session)` | `@pytest.mark.asyncio` | — |
| `test_iteration_restore_preserves_current_shared_absence` | *(async)* `(db_session)` | `@pytest.mark.asyncio` | — |
| `test_reassigning_allocation_does_not_transfer_private_absence` | *(async)* `(db_session)` | `@pytest.mark.asyncio` | — |
| `test_person_calendar_cannot_be_deleted_while_selected` | *(async)* `(db_session)` | `@pytest.mark.asyncio` | — |
| `test_overflow_forecast_cannot_commit_outside_allocation_dates` | *(async)* `(db_session)` | `@pytest.mark.asyncio` | — |
