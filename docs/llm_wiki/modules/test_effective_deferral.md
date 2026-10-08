# test_effective_deferral Module

**Path:** `backend/tests/test_effective_deferral.py`

## Description

Complete ancestry policy, working lifecycle parity and rejected-write atomicity.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `AuthorityError` |
| `app.commands` | `PlanningConflict` |
| `app.main` | `app` |
| `app.models.agent` | `TaskEvent` |
| `app.models.iteration` | `Iteration` |
| `app.models.outbound_webhook` | `OutboundWebhookEvent` |
| `app.models.recovery` | `ApplicationSnapshot` |
| `app.models.task` | `Task` |
| `app.models.task_status_log` | `TaskStatusLog` |
| `app.schemas.task` | `TaskCreate`, `TaskUpdate` |
| `app.schemas.task_domain` | `TaskActionRequest` |
| `app.services.task_domain_service` | `TaskDomainService` |
| `app.services.task_service` | `TaskService`, `TaskVersionConflictError` |
| `app.services.work_metrics` | `effective_work_flags` |
| `httpx` | `httpx` |
| `pytest` | `pytest` |
| `sqlalchemy` | `func`, `select`, `update` |
| `tests.test_delivery_scenarios` | `delivery_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_effective_deferral.py"]
    n1 --> n0
    click n1 "../modules/test_effective_deferral.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (15) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 15 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_unhydrated_parent_policy_fails_closed` | `()` | — | — |
| `test_reparenting_recomputes_inherited_deferral_without_copying_the_flag` | *(async)* `(delivery_store)` | — | — |
| `test_deep_ancestor_deferral_clearing_and_unscheduled_manual_freedom` | *(async)* `(delivery_store)` | — | — |
| `test_deferred_lifecycle_rejection_preserves_version_history_revisions_and_claims` | *(async)* `(delivery_store, transition)` | `@pytest.mark.parametrize('transition', ['active', 'resolved'])` | — |
| `test_stale_session_cannot_ignore_a_committed_ancestor_deferral` | *(async)* `(delivery_store)` | — | — |
| `test_cyclic_ancestry_is_a_typed_conflict_at_http_execution_boundary` | *(async)* `(delivery_store)` | — | — |
