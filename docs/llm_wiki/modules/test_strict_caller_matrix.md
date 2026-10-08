# test_strict_caller_matrix Module

**Path:** `backend/tests/test_strict_caller_matrix.py`

## Description

Operator caller observations are enforced in both dialects and sampled explicitly.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `mcp_agent_tools` |
| `app.authority` | `Authority` |
| `app.config` | `get_settings` |
| `app.main` | `app` |
| `app.models.agent` | `AgentActor` |
| `app.models.calendar` | `Calendar` |
| `app.models.identity` | `PrincipalProfileLink` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMemberProfileSkill`, `Vacation` |
| `app.mutation_versions` | `MissingMutationRevision` |
| `app.runtime_telemetry` | `metrics` |
| `app.services.snapshot_service` | `SnapshotService` |
| `app.services.task_service` | `TaskVersionConflictError` |
| `datetime` | `date`, `datetime`, `timezone` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `select` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `managed_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_strict_caller_matrix.py"]
    n1 --> n0
    click n1 "../modules/test_strict_caller_matrix.md"
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
| `missing_count` | `()` | — | — |
| `test_operator_caller_matrix` | *(async)* `(managed_store, monkeypatch, request, row)` | `@pytest.mark.parametrize('row', ROWS)` | — |
| `test_structural_commands_replays_and_rollback_keep_identity_and_versions` | *(async)* `(managed_store, monkeypatch, request)` | — | — |
| `test_empty_calendar_scope_detects_new_allocation_before_delete` | *(async)* `(managed_store, monkeypatch)` | — | — |
| `test_snapshot_restore_observes_revision_and_keeps_history` | *(async)* `(managed_store, monkeypatch)` | — | — |
| `test_mcp_positive_missing_and_stale_versions_share_policy` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_destructive_confirmation_preserves_original_scope` | *(async)* `(managed_store, monkeypatch, kind)` | `@pytest.mark.parametrize('kind', ['project', 'iteration'])` | — |
