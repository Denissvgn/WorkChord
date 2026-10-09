# test_planning_read_models Module

**Path:** `backend/tests/test_planning_read_models.py`

## Description

Independent synthetic counterexamples for read-model and inherited policy parity.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `PlanningConflict`, `command_transaction` |
| `app.models.calendar` | `Calendar` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMemberProfile`, `Vacation` |
| `app.services` | `project_service`, `work_metrics` |
| `app.services.capacity_service` | `CapacityService` |
| `app.services.iteration_service` | `IterationService` |
| `app.services.project_service` | `ProjectService` |
| `app.services.scheduler_service` | `IncrementalScheduler`, `SchedulerService` |
| `app.services.team_service` | `TeamService` |
| `datetime` | `UTC`, `date`, `datetime` |
| `pytest` | `pytest` |
| `sqlalchemy` | `select` |
| `tests.test_profile_capacity` | `allocation`, `db_session` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_planning_read_models.py"]
    n1 --> n0
    click n1 "../modules/test_planning_read_models.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (13) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_iteration_readiness_uses_actual_person_hours` | *(async)* `(db_session)` | — | — |
| `deferred_leaf` | *(async)* `(db)` | — | — |
| `test_schedule_preview_does_not_allocate_inherited_deferred_leaf` | *(async)* `(db_session)` | — | — |
| `test_capacity_projection_does_not_count_inherited_deferred_baseline` | *(async)* `(db_session)` | — | — |
| `test_incremental_schedule_excludes_inherited_deferred_work` | *(async)* `(db_session)` | — | — |
| `test_yaml_schedule_orders_inherited_optional_after_required_work` | *(async)* `(db_session)` | — | — |
| `test_readiness_reports_shared_booking_risk_without_private_task_details` | *(async)* `(db_session)` | — | — |
| `test_capacity_refuses_incomplete_ancestry_but_ignores_unrelated_scope` | *(async)* `(db_session)` | — | — |
| `test_project_target_risk_uses_declared_working_date` | `(monkeypatch, zone, expected_days)` | `@pytest.mark.parametrize('zone, expected_days', [('Asia/Tokyo', -1), ('America/Los_Angeles', 0)])` | — |
