# test_agent_model_catalog_api Module

**Path:** `backend/tests/test_agent_model_catalog_api.py`

## Description

Focused Wave 2 model administration and actor-roster qualification.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app` | `mcp_agent_tools` |
| `app.agent_contract` | `MODEL_AWARE_ROUTING_FEATURE`, `agent_contract_features` |
| `app.config` | `get_settings` |
| `app.database` | `get_db` |
| `app.main` | `app` |
| `app.mcp_server` | `_structured_tool_error`, `mcp` |
| `app.models.agent` | `AgentActor`, `AgentModelBinding`, `AgentModelCatalogEntry`, `AgentRun`, `AgentTaskAssignment`, `TaskEvent` |
| `app.models.team_member` | `TeamMemberProfile`, `TeamMemberProfileSkill` |
| `app.routers` | `agent`, `agent_planning` |
| `app.schemas.agent` | `AgentActorCreate`, `AgentTaskAssignmentCreate`, `AgentTaskAssignmentUpdate`, `AgentWorkBegin`, `ModelAwareAgentTaskAssignmentCreate`, `ModelAwareAgentTaskAssignmentUpdate`, `ModelAwareAgentWorkBegin` |
| `app.schemas.agent_planning` | `AgentPlanningCommandContext` |
| `app.schemas.agent_routing` | `AgentModelBindingDisable`, `AgentModelBindingUpdate`, `AgentModelCatalogUpdate` |
| `app.services.agent_model_catalog_service` | `AgentModelCatalogService`, `AgentModelConflictError` |
| `app.services.agent_routing_service` | `AgentRoutingConflictError` |
| `app.services.agent_service` | `AgentPermissionError`, `AgentService`, `hash_api_key` |
| `app.services.agent_work_service` | `AgentWorkService` |
| `app.utils.time` | `utc_now` |
| `datetime` | `UTC`, `datetime` |
| `fastapi` | `FastAPI`, `HTTPException` |
| `httpx` | `httpx` |
| `importlib.util` | `importlib.util` |
| `json` | `json` |
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `sqlalchemy` | `event`, `select` |
| `sqlalchemy.ext.asyncio` | `AsyncEngine`, `AsyncSession`, `async_sessionmaker` |
| `typing` | `Any` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_agent_model_catalog_api.py"]
    n1 --> n0
    click n1 "../modules/test_agent_model_catalog_api.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (18) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 4 | 1 |

> All 18 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_catalog_values` | `(key: str = 'balanced-code', **overrides: Any) -> dict[str, Any]` | — | — |
| `_command` | `(key: str) -> AgentPlanningCommandContext` | — | — |
| `_headers` | `(api_key: str, command_key: str \| None = None) -> dict[str, str]` | — | — |
| `_assert_secret_free` | `(value: Any) -> None` | — | — |
| `test_model_updates_reject_null_for_non_nullable_fields` | `(schema, payload: dict[str, Any]) -> None` | `@pytest.mark.parametrize(('schema', 'payload'), ((AgentModelCatalogUpdate, {'expected_revision': 1, 'provider': None}), (AgentModelBindingUpdate, {'expected_revision': 1, 'tool_tags': None})))` | — |
| `_http_client` | *(async)* `(app: FastAPI, db: AsyncSession) -> httpx.AsyncClient` | — | — |
| `test_rest_and_mcp_model_authorization_idempotency_and_conflicts` | *(async)* `(db_session: AsyncSession) -> None` | `@pytest.mark.sqlite`, `@pytest.mark.asyncio` | — |
| `test_binding_disable_requires_explicit_reconciliation_and_marks_queue_stale` | *(async)* `(db_session: AsyncSession, actor_factory, task_factory) -> None` | `@pytest.mark.sqlite`, `@pytest.mark.asyncio` | — |
| `test_rest_and_mcp_rosters_are_identical_and_secret_free` | *(async)* `(db_session: AsyncSession) -> None` | `@pytest.mark.sqlite`, `@pytest.mark.asyncio` | — |
| `_seed_roster_actors` | *(async)* `(db: AsyncSession, *, catalog_id: int, start: int, count: int) -> None` | — | — |
| `_roster_query_count` | *(async)* `(factory: async_sessionmaker[AsyncSession], engine: AsyncEngine) -> tuple[int, int]` | — | — |
| `test_roster_query_count_is_cardinality_constant` | *(async)* `(db_session_factory: async_sessionmaker[AsyncSession], sqlite_engine: AsyncEngine) -> None` | `@pytest.mark.sqlite`, `@pytest.mark.asyncio` | — |
| `test_actor_provisioning_payload_accepts_catalog_key_and_rejects_secrets` | `(monkeypatch: pytest.MonkeyPatch) -> None` | — | — |
| `test_actor_provisioning_creates_binding_and_audit_atomically` | *(async)* `(db_session: AsyncSession, actor_factory) -> None` | `@pytest.mark.sqlite`, `@pytest.mark.asyncio` | — |
| `test_wave3_surfaces_advertise_model_aware_routing` | `() -> None` | `@pytest.mark.contract` | — |
| `test_mcp_registers_roster_catalog_resources_and_admin_tools` | *(async)* `() -> None` | `@pytest.mark.contract`, `@pytest.mark.asyncio` | — |
| `test_mcp_assignment_and_begin_payloads_preserve_additive_legacy_union` | `() -> None` | `@pytest.mark.contract` | — |
| `test_routing_conflicts_keep_structured_detail_across_rest_and_mcp` | `() -> None` | `@pytest.mark.contract` | — |
