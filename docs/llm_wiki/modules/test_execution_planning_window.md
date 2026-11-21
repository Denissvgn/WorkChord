# test_execution_planning_window Module

**Path:** `backend/tests/test_execution_planning_window.py`

## Description

Date-only planning reservations retain verifiable work without weakening task writes.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `command` |
| `app` | `mcp_server` |
| `app.agent_contract` | `EXECUTION_PLANNING_WINDOW_FEATURE` |
| `app.config` | `get_settings` |
| `app.main` | `app` |
| `app.models.agent` | `AgentIdempotencyRecord`, `AgentModelCatalogEntry`, `AgentRun`, `AgentTaskAssignment`, `TaskEvent`, `AgentActor`, `AgentTeamTopologyMember` |
| `app.models.identity` | `CommandAudit`, `Principal`, `ProjectMembership`, `WorkspaceMembership` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.recovery` | `ApplicationSnapshot` |
| `app.models.task` | `Task` |
| `app.schemas.agent_team_setup` | `AgentTeamRuntimeAcknowledgement` |
| `app.services` | `planning_window_reconciliation`, `planning_window_reconciliation`, `retained_planning_output`, `planning_window_reconciliation` |
| `app.services.agent_service` | `hash_api_key` |
| `app.services.agent_team_setup_service` | `AgentTeamSetupService` |
| `app.services.execution_planning_window` | `digest`, `seal_authority` |
| `app.services.identity_service` | `IdentityService`, `initialize_control_plane` |
| `app.services.retained_planning_output` | `_authenticate_checkpoint` |
| `app.services.upgrade_service` | `alembic_config` |
| `asyncio` | `asyncio` |
| `contextlib` | `nullcontext` |
| `copy` | `deepcopy` |
| `datetime` | `datetime`, `timedelta`, `timezone`, `date` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `event`, `select`, `text`, `update`, `create_engine` |
| `sqlalchemy.exc` | `DBAPIError` |
| `tests` | `test_team_pm_dispatch` |
| `tests.test_agent_team_setup_qualification` | `provision_ready_topology`, `routing_base` |
| `tests.test_review_provenance_transports` | `databases`, `fence` |
| `tests.test_team_pm_recovery` | `recovery_api` |
| `time` | `perf_counter_ns` |
| `types` | `SimpleNamespace` |
| `unittest.mock` | `patch` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_execution_planning_window.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/test_execution_planning_window.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (1) |
| Outbound | `backend` (22) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 4 | 1 |

> All 23 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_cached_snapshot_requires_the_actual_unchanged_payload_bytes` | `(tmp_path)` | — | — |
| `measured_pending_polls` | *(async)* `(call, work, worker_key, db, record_property)` | — | — |
| `test_nullable_window_migration_preserves_the_prior_run` | `(dialect, request, tmp_path, configure_database)` | `@pytest.mark.parametrize('dialect', [pytest.param('sqlite', marks=pytest.mark.sqlite), pytest.param('postgresql', marks=(pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network))])` | — |
| `planning_patch` | *(async)* `(client, pm, iteration, revision, key, **changes)` | — | — |
| `operator_call` | *(async)* `(http, transport, credential, task, receipt, *, apply = False, expected = None, key = None, denied = None)` | — | — |
| `worker_attest` | *(async)* `(http, transport, key, run_id, body, request_key, *, error = None)` | — | — |
| `competing_updates` | *(async)* `(factory, task, assignment_id, *, blocked, run_id = None)` | — | — |
| `cancel_unconfirmable` | *(async)* `(http, transport, pm_key, assignment, queue_revision)` | — | — |
| `test_date_only_reservation` | *(async)* `(db_session, db_session_factory, task_factory, team_member_factory, actor_factory, monkeypatch, transport, case, record_property)` | `@databases`, `@pytest.mark.parametrize('transport', ['rest', 'mcp'])`, `@pytest.mark.parametrize('case', ['running', 'verification', 'rework', 'substantive', 'legacy_running', 'legacy_refresh', 'legacy_verification', 'legacy_rework', 'legacy_recovered_rework', 'legacy_missing', 'legacy_stale', 'legacy_scope', 'authority_changed', 'artifact_changed', 'consecutive_extensions', 'legacy_drained', 'legacy_unconfirmable', 'legacy_no_checkpoint', 'queued_normal', 'queued_recovery', 'legacy_queued_normal', 'legacy_queued_recovery'])`, `@pytest.mark.usefixtures('deployed_agent_skill_release')` | — |
