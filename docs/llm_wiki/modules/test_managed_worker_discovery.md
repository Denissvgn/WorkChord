# test_managed_worker_discovery Module

**Path:** `backend/tests/test_managed_worker_discovery.py`

## Description

Managed discovery attribution, scope and transaction boundaries for assigned workers.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `Authority`, `AuthorityError` |
| `app.commands` | `command_transaction`, `current_command` |
| `app.config` | `get_settings` |
| `app.main` | `app` |
| `app.models.agent` | `AgentActor`, `AgentIdempotencyRecord`, `TaskEvent` |
| `app.models.identity` | `CommandAudit`, `Principal`, `ProjectMembership`, `WorkspaceMembership` |
| `app.models.task` | `Task` |
| `app.models.triage` | `TriageItem` |
| `app.schemas.agent` | `AgentDiscoveryTriageCreate` |
| `app.services.agent_work_service` | `AgentWorkService` |
| `app.services.identity_service` | `IdentityService`, `initialize_control_plane` |
| `app.services.triage_service` | `TriageService` |
| `collections.abc` | `AsyncIterator` |
| `contextlib` | `asynccontextmanager`, `nullcontext` |
| `dataclasses` | `dataclass` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `func`, `select` |
| `sqlalchemy.exc` | `DBAPIError` |
| `sqlalchemy.ext.asyncio` | `AsyncSession`, `async_sessionmaker` |
| `tests.test_agent_discovery_report` | `WORKER_SCOPES`, `begin_as_worker`, `discovery_body`, `frozen_working_day` |
| `tests.test_delivery_scenarios` | `delivery_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_managed_worker_discovery.py"]
    n1 --> n0
    click n1 "../modules/test_managed_worker_discovery.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (14) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 14 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [AssignedWorker](../entities/AssignedWorker.md) | 42 | — | — |
| [PlannedRollback](../entities/PlannedRollback.md) | 204 | `Exception` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `reset_cached_settings` | `()` | `@pytest.fixture(autouse=True)` | — |
| `worker` | *(async)* `(delivery_store, frozen_working_day, monkeypatch) -> AsyncIterator[AssignedWorker]` | `@pytest.fixture` | — |
| `test_managed_assigned_discovery_replays_once_and_keeps_the_executor_audit` | *(async)* `(worker)` | — | — |
| `test_managed_executor_consumes_one_matching_triage_item` | *(async)* `(worker, case)` | `@pytest.mark.parametrize('case', ['matching', 'second_item', 'wrong_iteration', 'different_actor', 'missing_scope', 'viewer'])` | — |
| `test_discovery_marker_ends_with_its_command` | *(async)* `(worker, outcome)` | `@pytest.mark.parametrize('outcome', ['commit', 'rollback', 'preview'])` | — |
| `test_discovery_and_pm_recovery_lock_the_same_task_until_the_insert_is_flushed` | *(async)* `(worker, monkeypatch)` | — | — |
