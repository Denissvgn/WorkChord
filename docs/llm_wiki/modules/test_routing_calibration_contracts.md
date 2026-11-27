# test_routing_calibration_contracts Module

**Path:** `backend/tests/test_routing_calibration_contracts.py`

## Description

Calibration contracts: submitted, approved and read under deployment-operator authority.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `alembic` | `command` |
| `app.config` | `get_settings` |
| `app.database` | `get_db` |
| `app.main` | `app` |
| `app.models.agent` | `AgentActor`, `TaskEvent` |
| `app.models.identity` | `Principal`, `WorkspaceAuthorityState`, `WorkspaceMembership` |
| `app.models.routing_calibration` | `RoutingCalibrationContractRevision` |
| `app.models.routing_qualification` | `RoutingQualificationKey` |
| `app.schemas.agent_planning` | `AgentPlanningCommandContext` |
| `app.schemas.routing_calibration` | `RoutingCalibrationContractSubmit`, `RoutingCalibrationContractTerms`, `RoutingCalibrationContractApprove` |
| `app.schemas.routing_qualification` | `RoutingQualificationKeyRetire` |
| `app.services.agent_model_catalog_service` | `AgentModelConflictError` |
| `app.services.agent_service` | `hash_api_key` |
| `app.services.routing_calibration_contract_service` | `RoutingCalibrationContractService`, `approved_calibration_contract_count` |
| `app.services.routing_qualification_key_service` | `RoutingQualificationKeyService` |
| `app.services.upgrade_service` | `alembic_config` |
| `copy` | `deepcopy` |
| `datetime` | `UTC`, `datetime`, `timedelta` |
| `fastapi` | `FastAPI` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pydantic` | `ValidationError` |
| `pytest` | `pytest` |
| `sqlalchemy` | `select`, `create_engine` |
| `sqlalchemy.ext.asyncio` | `AsyncSession`, `AsyncSession`, `create_async_engine` |
| `typing` | `Any` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_routing_calibration_contracts.py"]
    n1 --> n0
    click n1 "../modules/test_routing_calibration_contracts.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (15) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 6 | 1 |

> All 15 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_terms` | `(**overrides: Any) -> dict[str, Any]` | — | — |
| `_headers` | `(api_key: str, command_key: str \| None = None, reason: str = 'Operator calibration change.') -> dict[str, str]` | — | — |
| `_client` | *(async)* `(app: FastAPI, db: AsyncSession) -> httpx.AsyncClient` | — | — |
| `_setup` | *(async)* `(db: AsyncSession) -> None` | — | — |
| `test_the_schema_refuses_terms_without_sample_bounds_decay_bias_review_or_approver` | `() -> None` | — | — |
| `test_the_terms_digest_is_canonical` | `() -> None` | — | — |
| `test_a_contract_is_submitted_approved_and_every_revision_is_kept` | *(async)* `(db_session: AsyncSession) -> None` | `@pytest.mark.sqlite`, `@pytest.mark.asyncio` | — |
| `test_approval_refuses_terms_naming_a_key_retired_since_submission` | *(async)* `(db_session: AsyncSession) -> None` | `@pytest.mark.sqlite`, `@pytest.mark.asyncio` | — |
| `_operator_state` | *(async)* `(db: AsyncSession) -> None` | — | — |
| `_command` | `(key: str) -> dict[str, str]` | — | — |
| `test_the_operator_admin_key_submits_and_approves_and_is_recorded_as_the_operator` | *(async)* `(db_session: AsyncSession, monkeypatch: pytest.MonkeyPatch, auth_mode: str) -> None` | `@pytest.mark.sqlite`, `@pytest.mark.asyncio`, `@pytest.mark.parametrize('auth_mode', ['managed', 'trusted_local'])` | — |
| `test_in_managed_mode_only_an_agent_with_an_operator_membership_approves` | *(async)* `(db_session: AsyncSession, monkeypatch: pytest.MonkeyPatch) -> None` | `@pytest.mark.sqlite`, `@pytest.mark.asyncio` | — |
| `test_a_key_named_by_a_contract_cannot_be_retired` | *(async)* `(db_session: AsyncSession) -> None` | `@pytest.mark.sqlite`, `@pytest.mark.asyncio` | — |
| `test_contracts_are_submitted_approved_and_read_on_postgresql` | *(async)* `(postgres_database, configure_database) -> None` | `@pytest.mark.postgresql`, `@pytest.mark.integration`, `@pytest.mark.allow_network`, `@pytest.mark.asyncio` | — |
