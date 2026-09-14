# test_postgresql_concurrency Module

**Path:** `backend/tests/database/test_postgresql_concurrency.py`

## Description

DBM-RUN-001 real-PostgreSQL concurrency and invariant matrix.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.config` | `get_settings` |
| `app.database_config` | `parse_database_configuration` |
| `app.models.agent` | `AgentActor`, `AgentIdempotencyRecord`, `AgentRun`, `AgentTaskAssignment` |
| `app.models.calendar` | `Calendar` |
| `app.models.iteration` | `Iteration` |
| `app.models.outbound_webhook` | `OutboundWebhookDelivery`, `OutboundWebhookDeliveryStatus`, `OutboundWebhookEvent` |
| `app.models.task` | `Task` |
| `app.models.triage` | `TriageItem`, `TriageItemStatus` |
| `app.services.agent_planning_service` | `AgentPlanningService` |
| `app.services.outbound_webhook_service` | `OutboundWebhookService` |
| `app.services.task_service` | `TaskService`, `TaskVersionConflictError` |
| `app.services.upgrade_service` | `bootstrap_database_schema` |
| `app.sql_semantics` | `portable_contains` |
| `app.utils.time` | `utc_now` |
| `asyncio` | `asyncio` |
| `datetime` | `date`, `timedelta` |
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `pytest_asyncio` | `pytest_asyncio` |
| `sqlalchemy` | `Column`, `Integer`, `MetaData`, `String`, `Table`, `func`, `select`, `text`, `update` |
| `sqlalchemy.exc` | `DBAPIError`, `IntegrityError` |
| `sqlalchemy.ext.asyncio` | `AsyncEngine`, `AsyncSession`, `async_sessionmaker`, `create_async_engine` |
| `tests.support` | `AsyncBarrier` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/database/test_postgresql_concurrency.py"]
    n1 --> n0
    click n1 "../modules/test_postgresql_concurrency.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (15) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 2 |

> All 15 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `postgresql_session_factory` | *(async)* `(postgres_database, configure_database) -> async_sessionmaker[AsyncSession]` | `@pytest_asyncio.fixture` | — |
| `_seed_race_workspace` | *(async)* `(factory: async_sessionmaker[AsyncSession]) -> dict[str, object]` | — | — |
| `_task_version_attempt` | *(async)* `(factory: async_sessionmaker[AsyncSession], task_id: int, barrier: AsyncBarrier) -> str` | — | — |
| `_insert_assignment` | *(async)* `(factory: async_sessionmaker[AsyncSession], *, task_id: int, actor_id: int, barrier: AsyncBarrier) -> str` | — | — |
| `_insert_run` | *(async)* `(factory: async_sessionmaker[AsyncSession], *, task_id: int, actor_id: int, assignment_id: int, barrier: AsyncBarrier) -> str` | — | — |
| `_record_planning_command` | *(async)* `(factory: async_sessionmaker[AsyncSession], *, actor_id: int, task_id: int, barrier: AsyncBarrier) -> str` | — | — |
| `test_postgresql_race_matrix_preserves_all_invariants` | *(async)* `(postgresql_session_factory: async_sessionmaker[AsyncSession], postgres_database) -> None` | `@pytest.mark.postgresql`, `@pytest.mark.integration`, `@pytest.mark.allow_network`, `@pytest.mark.asyncio` | — |
| `test_schedule_locks_are_iteration_scoped` | *(async)* `(postgresql_session_factory: async_sessionmaker[AsyncSession]) -> None` | `@pytest.mark.postgresql`, `@pytest.mark.integration`, `@pytest.mark.allow_network`, `@pytest.mark.asyncio` | Different aggregates proceed while the same aggregate is serialized. |
| `test_schedule_lock_implementation_has_no_global_table_lock` | `() -> None` | — | — |
| `test_global_lock_order_is_documented_and_implemented` | `() -> None` | — | — |
