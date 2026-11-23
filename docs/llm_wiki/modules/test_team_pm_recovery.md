# test_team_pm_recovery Module

**Path:** `backend/tests/test_team_pm_recovery.py`

## Description

Authenticated recovery and claim-fenced blocker reporting.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `database`, `mcp_server` |
| `app.config` | `get_settings` |
| `app.main` | `app` |
| `app.models.agent` | `AgentActor`, `AgentRun`, `AgentTaskAssignment`, `TaskEvent` |
| `app.models.capacity` | `PlanningState` |
| `app.models.identity` | `ProjectMembership`, `WorkspaceMembership` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.services.identity_service` | `IdentityService`, `initialize_control_plane` |
| `contextlib` | `asynccontextmanager`, `nullcontext` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `select` |
| `tests.test_agent_team_setup_qualification` | `provision_ready_topology`, `routing_base` |
| `tests.test_team_pm_dispatch` | `db_session_factory` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_team_pm_recovery.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/test_team_pm_recovery.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (6) |
| Outbound | `backend` (13) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 19 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `recovery_api` | *(async)* `(transport, factory, monkeypatch)` | `@asynccontextmanager` | — |
| `test_controller_recovers_once_and_worker_begins` | *(async)* `(db_session, db_session_factory, team_member_factory, task_factory, transport, auth_mode, monkeypatch)` | `@pytest.mark.usefixtures('deployed_agent_skill_release')`, `@pytest.mark.parametrize('transport', ['rest', 'mcp'])`, `@pytest.mark.parametrize('auth_mode', ['trusted_local', 'managed'])`, `@pytest.mark.parametrize('db_session_factory', [pytest.param('sqlite', marks=pytest.mark.sqlite), pytest.param('postgresql', marks=[pytest.mark.postgresql, pytest.mark.allow_network])], indirect=True)` | — |
| `test_recovery_retains_ownership_outside_the_controller_team` | *(async)* `(db_session, db_session_factory, team_member_factory, task_factory, actor_factory, monkeypatch, foreign_owner)` | `@pytest.mark.sqlite`, `@pytest.mark.usefixtures('deployed_agent_skill_release')`, `@pytest.mark.parametrize('foreign_owner', ['assignment', 'run', 'claim'])` | — |
| `test_recovery_moves_stale_team_ownership_without_lowering_model_review` | *(async)* `(db_session, db_session_factory, team_member_factory, task_factory, monkeypatch)` | `@pytest.mark.sqlite`, `@pytest.mark.usefixtures('deployed_agent_skill_release')` | — |
