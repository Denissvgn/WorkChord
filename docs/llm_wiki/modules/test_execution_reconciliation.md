# test_execution_reconciliation Module

**Path:** `backend/tests/test_execution_reconciliation.py`

## Description

Operator reconciliation through authenticated REST and registered MCP commands.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `database`, `mcp_server` |
| `app.config` | `get_settings` |
| `app.main` | `app` |
| `app.models.agent` | `AgentRun`, `TaskEvent` |
| `app.models.identity` | `CommandAudit`, `Principal`, `ProjectMembership`, `WorkspaceMembership` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.services` | `agent_work_service`, `execution_reconciliation` |
| `app.services.agent_service` | `hash_api_key` |
| `app.services.execution_reconciliation` | `ACTION` |
| `app.services.identity_service` | `IdentityService`, `initialize_control_plane` |
| `app.utils.time` | `utc_now` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `func`, `select` |
| `tests.test_agent_model_catalog_api` | `_catalog_values`, `_command_headers` |
| `tests.test_agent_team_setup_qualification` | `acknowledge_member`, `provision_ready_topology`, `routing_base` |
| `tests.test_team_pm_dispatch` | `assignment_api`, `db_session_factory` |
| `tests.test_team_pm_recovery` | `recovery_api` |
| `types` | `SimpleNamespace` |
| `unittest.mock` | `AsyncMock` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_execution_reconciliation.py"]
    n1 --> n0
    click n1 "../modules/test_execution_reconciliation.md"
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
| `test_reconciliation_uses_operator_and_archived_catalog` | *(async)* `(db_session, db_session_factory, actor_factory, team_member_factory, task_factory, monkeypatch, auth_mode, change_before_begin)` | `@pytest.mark.asyncio`, `@database_engines`, `@pytest.mark.usefixtures('deployed_agent_skill_release')`, `@pytest.mark.parametrize('auth_mode', ['managed', 'trusted_local'])`, `@pytest.mark.parametrize('change_before_begin', [False, True], ids=['historical-match', 'changed-at-start'])` | — |
| `test_legacy_acknowledgement_without_binding_revisions_stays_unknown` | *(async)* `()` | `@pytest.mark.asyncio` | — |
