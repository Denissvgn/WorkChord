# test_allocation_recovery Module

**Path:** `backend/tests/test_allocation_recovery.py`

## Description

Allocation membership recovery preserves durable references and rolls back failures.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `Authority` |
| `app.commands` | `PlanningConflict` |
| `app.main` | `app` |
| `app.models.agent` | `AgentTaskAssignment` |
| `app.models.identity` | `WorkspaceAuthorityState` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.recovery` | `ApplicationSnapshot` |
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile` |
| `app.schemas.team` | `TeamMemberCreate` |
| `app.services.snapshot_service` | `SnapshotService` |
| `app.services.task_brief_service` | `TaskBriefService` |
| `app.services.team_service` | `TeamService` |
| `httpx` | `httpx` |
| `pytest` | `pytest` |
| `sqlalchemy` | `func`, `select`, `text` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `managed_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_allocation_recovery.py"]
    n1 --> n0
    click n1 "../modules/test_allocation_recovery.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (16) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 16 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `capture_then_add` | *(async)* `(factory, scenario)` | — | — |
| `test_extra_allocation_detaches_but_global_owner_and_profile_identity_survive` | *(async)* `(delivery_store)` | — | — |
| `test_incompatible_allocation_reference_rejects_before_recovery_changes` | *(async)* `(delivery_store, reference)` | `@pytest.mark.parametrize('reference', ['external_task', 'queued_assignment'])` | — |
| `test_failure_after_detach_restores_membership_and_retains_recovery_history` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_unknown_physical_allocation_reference_fails_closed` | *(async)* `(delivery_store)` | — | — |
| `test_saved_allocation_external_reference_is_preflighted_too` | *(async)* `(delivery_store)` | — | — |
| `test_operator_rest_restore_reconciles_exact_allocation_membership` | *(async)* `(managed_store)` | — | — |
