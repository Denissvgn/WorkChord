# test_postponed_out_of_scheduling Module

**Path:** `backend/tests/test_postponed_out_of_scheduling.py`

## Description

Postponed work keeps its last dates as history: it is never scheduled, counted, ready, dispatched or verified.

## Imports

| Source | Symbols |
|--------|---------|
| `app.main` | `app` |
| `app.models.release` | `Release` |
| `app.models.task` | `Task`, `TaskDependency` |
| `app.schemas.agent` | `AgentTaskAssignmentCreate` |
| `app.services.agent_readiness` | `evaluate_agent_readiness` |
| `app.services.agent_routing_service` | `AgentRoutingConflictError` |
| `app.services.agent_service` | `AgentService` |
| `app.services.agent_work_service` | `AgentConflictError`, `AgentWorkService` |
| `app.services.capacity_service` | `CapacityService` |
| `app.services.iteration_service` | `IterationService` |
| `app.services.release_service` | `ReleaseService` |
| `app.services.review_provenance` | `select_reviewer` |
| `app.services.scheduler_service` | `SchedulerService` |
| `app.services.team_service` | `TeamService` |
| `app.services.work_metrics` | `aggregate_metrics`, `leaf_metrics`, `task_signals` |
| `datetime` | `date` |
| `httpx` | `httpx` |
| `pytest` | `pytest` |
| `sqlalchemy` | `select` |
| `tests.test_agent_routing_service` | `_rollout`, `_routing_fixture` |
| `tests.test_delivery_scenarios` | `delivery_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_postponed_out_of_scheduling.py"]
    n1 --> n0
    click n1 "../modules/test_postponed_out_of_scheduling.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (17) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 17 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `january_today` | `(monkeypatch)` | `@pytest.fixture` | — |
| `_postponed_plan` | *(async)* `(db, scenario)` | — | In the second seeded iteration: postponed work holding two old days, planned work and its dependent. |
| `_assert_schedule_skips_postponed` | `(result, postponed_id, planned_id, dependent_id)` | — | — |
| `test_schedule_run_frees_postponed_capacity_and_waits_dependents_on_it` | *(async)* `(delivery_store, january_today)` | — | — |
| `test_schedule_preview_skips_postponed_work` | *(async)* `(delivery_store, january_today)` | — | — |
| `test_postponed_work_commits_no_capacity` | *(async)* `(delivery_store)` | — | — |
| `_readiness` | `(task, dependencies = ())` | — | — |
| `test_readiness_names_postponed_as_the_blocker_and_waits_dependents_on_it_by_name` | `()` | — | — |
| `test_dispatch_never_offers_or_assigns_postponed_work` | *(async)* `(db_session, profile_factory, actor_factory, team_member_factory, task_factory)` | — | — |
| `test_no_verifier_can_be_selected_for_postponed_work` | *(async)* `()` | — | — |
| `test_postponed_task_raises_no_schedule_signal` | `()` | — | — |
| `test_leaf_metrics_count_postponed_apart_from_other_statuses` | `()` | — | — |
| `test_iteration_and_release_progress_count_postponed_separately` | *(async)* `(delivery_store)` | — | — |
| `test_dependent_with_saved_dates_and_its_own_cause_keeps_dates_and_waits_on_postponed_work` | *(async)* `(delivery_store, january_today)` | — | — |
| `test_dependency_on_a_summary_waits_on_its_postponed_child` | *(async)* `(delivery_store, january_today)` | — | — |
| `test_readiness_names_postponed_work_below_a_summary_prerequisite` | `()` | — | — |
