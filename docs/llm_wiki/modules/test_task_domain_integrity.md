# test_task_domain_integrity Module

**Path:** `backend/tests/test_task_domain_integrity.py`

## Description

Task context, recovery and project projections stay consistent across commands.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `Authority`, `AuthorityError` |
| `app.commands` | `command_transaction` |
| `app.config` | `get_settings` |
| `app.models.calendar` | `Calendar` |
| `app.models.identity` | `Principal` |
| `app.models.recovery` | `ApplicationSnapshot`, `TaskDeletionFence`, `TaskDeletionFence` |
| `app.models.task` | `Task`, `TaskDependency` |
| `app.models.task_brief` | `TaskProgressRecord` |
| `app.schemas.iteration` | `IterationUpdate` |
| `app.schemas.task` | `TaskCreate`, `TaskUpdate` |
| `app.schemas.task_brief` | `BriefCriterion`, `CriterionProgress`, `ProgressWrite`, `TaskBrief`, `TaskReviewWrite` |
| `app.schemas.task_domain` | `TaskActionRequest` |
| `app.services.backlog_snapshot_service` | `BacklogSnapshotService` |
| `app.services.iteration_service` | `IterationService` |
| `app.services.project_service` | `ProjectService` |
| `app.services.snapshot_service` | `SnapshotService` |
| `app.services.task_brief_service` | `TaskBriefService` |
| `app.services.task_domain_service` | `TaskDomainService` |
| `app.services.task_service` | `TaskService`, `TaskVersionConflictError` |
| `app.services.work_metrics` | `aggregate_metrics` |
| `asyncio` | `asyncio` |
| `dataclasses` | `replace` |
| `pytest` | `pytest` |
| `sqlalchemy` | `delete`, `func`, `select` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_task_domain` | `human_context` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_task_domain_integrity.py"]
    n1 --> n0
    click n1 "../modules/test_task_domain_integrity.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (22) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

> All 22 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_nested_backlog_participates_in_project_and_milestone_metrics` | *(async)* `(delivery_store)` | — | — |
| `test_blocked_metrics_include_explicit_and_canceled_dependencies` | *(async)* `(delivery_store)` | — | — |
| `test_blocked_metrics_do_not_hide_inaccessible_prerequisites` | *(async)* `(delivery_store)` | — | — |
| `test_dependency_mutations_invalidate_evidence_without_erasing_history` | *(async)* `(delivery_store, operation)` | `@pytest.mark.parametrize('operation', ['add', 'remove', 'update_add', 'update_remove'])` | — |
| `test_backlog_project_move_rejects_crossing_edges_atomically` | *(async)* `(delivery_store, moving_prerequisite)` | `@pytest.mark.parametrize('moving_prerequisite', [False, True])` | — |
| `test_backlog_subtree_move_preserves_internal_edges_and_captures_both_scopes` | *(async)* `(delivery_store)` | — | — |
| `test_backlog_move_requires_permission_in_both_projects` | *(async)* `(delivery_store)` | — | — |
| `test_restore_advances_above_deleted_version_and_rejects_stale_writes` | *(async)* `(delivery_store, backlog)` | `@pytest.mark.parametrize('backlog', [False, True])` | — |
| `test_restore_rejects_missing_historical_deletion_fence` | *(async)* `(delivery_store, backlog)` | `@pytest.mark.parametrize('backlog', [False, True])` | — |
| `test_calendar_switch_preserves_hours_and_refreshes_day_units` | *(async)* `(delivery_store, hours)` | `@pytest.mark.parametrize('hours', [None, 0, 1.5, 8])` | — |
| `test_subtree_deletion_fences_survive_rollback_and_repeated_restoration` | *(async)* `(delivery_store, backlog)` | `@pytest.mark.parametrize('backlog', [False, True])` | — |
| `test_restore_removals_record_deletion_fences` | *(async)* `(delivery_store)` | — | — |
| `test_project_move_rolls_back_both_scope_snapshots_on_failure` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_opposite_backlog_moves_use_one_project_lock_order` | *(async)* `(delivery_store)` | — | — |
| `test_scoped_snapshot_retention_keeps_human_commands_available` | *(async)* `(delivery_store, monkeypatch, scope)` | `@pytest.mark.parametrize('scope', ['iteration', 'backlog'])` | — |
