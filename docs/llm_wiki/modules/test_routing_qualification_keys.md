# test_routing_qualification_keys Module

**Path:** `backend/tests/test_routing_qualification_keys.py`

## Description

The deployment's governed qualification key registry and the keys catalog entries hold.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `alembic` | `command`, `command` |
| `app.config` | `get_settings` |
| `app.database` | `get_db` |
| `app.main` | `app` |
| `app.models.agent` | `AgentActor`, `TaskEvent`, `AgentModelCatalogEntry`, `TaskRoutingAssessment`, `AgentModelCatalogEntry` |
| `app.models.identity` | `Principal`, `WorkspaceAuthorityState` |
| `app.models.project` | `Project` |
| `app.models.routing_qualification` | `RoutingQualificationKeyRevision`, `RoutingQualificationKey`, `RoutingQualificationKey` |
| `app.models.task` | `Task` |
| `app.schemas.agent_planning` | `AgentPlanningCommandContext` |
| `app.schemas.agent_routing` | `RequiredModelEnvelope` |
| `app.schemas.routing_qualification` | `RoutingQualificationKeyRetire` |
| `app.services.agent_model_catalog_service` | `AgentModelConflictError` |
| `app.services.agent_routing_policy` | `ROUTING_SKILL_KEYS`, `UnknownRoutingKeyError`, `evaluate_model_envelope`, `known_routing_keys`, `require_known_routing_keys` |
| `app.services.agent_service` | `hash_api_key` |
| `app.services.routing_qualification_key_service` | `RoutingQualificationKeyService`, `require_known_qualification_keys`, `RoutingQualificationKeyService`, `require_known_qualification_keys` |
| `app.services.upgrade_service` | `alembic_config`, `alembic_config` |
| `asyncio` | `asyncio` |
| `fastapi` | `FastAPI` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `select`, `create_engine`, `create_engine` |
| `sqlalchemy.ext.asyncio` | `AsyncSession`, `AsyncSession`, `create_async_engine`, `AsyncSession`, `create_async_engine` |
| `typing` | `Any` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_routing_qualification_keys.py"]
    n1 --> n0
    click n1 "../modules/test_routing_qualification_keys.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (16) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 5 | 1 |

> All 16 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_catalog_values` | `(key: str, **overrides: Any) -> dict[str, Any]` | — | — |
| `_headers` | `(api_key: str, command_key: str \| None = None, reason: str = 'Operator qualification change.') -> dict[str, str]` | — | — |
| `_client` | *(async)* `(app: FastAPI, db: AsyncSession) -> httpx.AsyncClient` | — | — |
| `_actors` | *(async)* `(db: AsyncSession) -> None` | — | — |
| `test_policy_accepts_declared_keys_beside_the_fixed_built_in_keys` | `() -> None` | — | — |
| `test_required_envelope_omits_empty_qualification_keys_from_its_stored_shape` | `() -> None` | — | — |
| `test_operator_declares_revises_and_retires_a_key_with_audited_revisions` | *(async)* `(db_session: AsyncSession) -> None` | `@pytest.mark.sqlite`, `@pytest.mark.asyncio` | — |
| `test_catalog_entries_hold_declared_keys_and_an_effort_change_clears_them` | *(async)* `(db_session: AsyncSession) -> None` | `@pytest.mark.sqlite`, `@pytest.mark.asyncio` | — |
| `test_usage_and_share_locked_validation_work_on_postgresql` | *(async)* `(postgres_database, configure_database) -> None` | `@pytest.mark.postgresql`, `@pytest.mark.integration`, `@pytest.mark.allow_network`, `@pytest.mark.asyncio` | — |
| `test_retire_and_validation_serialize_across_postgresql_sessions` | *(async)* `(postgres_database, configure_database) -> None` | `@pytest.mark.postgresql`, `@pytest.mark.integration`, `@pytest.mark.allow_network`, `@pytest.mark.asyncio` | — |
| `test_the_operator_admin_key_governs_the_registry_and_no_credential_is_refused` | *(async)* `(db_session: AsyncSession, monkeypatch: pytest.MonkeyPatch, auth_mode: str) -> None` | `@pytest.mark.sqlite`, `@pytest.mark.asyncio`, `@pytest.mark.parametrize('auth_mode', ['managed', 'trusted_local'])` | — |
