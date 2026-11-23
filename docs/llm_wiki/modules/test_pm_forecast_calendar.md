# test_pm_forecast_calendar Module

**Path:** `backend/tests/test_pm_forecast_calendar.py`

## Description

A managed planning principal can forecast an iteration using a single annual calendar.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `database`, `mcp_server` |
| `app.config` | `get_settings` |
| `app.main` | `app` |
| `app.models.calendar` | `Calendar` |
| `app.models.identity` | `ProjectMembership`, `WorkspaceMembership` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.services.identity_service` | `IdentityService`, `initialize_control_plane` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pytest` | `pytest` |
| `tests` | `test_team_pm_dispatch` |
| `tests.test_agent_team_setup_qualification` | `provision_ready_topology`, `routing_base` |
| `tests.test_review_provenance_transports` | `databases` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_pm_forecast_calendar.py"]
    n1 --> n0
    click n1 "../modules/test_pm_forecast_calendar.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (12) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_scoped_single_year_forecast` | *(async)* `(db_session, db_session_factory, team_member_factory, task_factory, monkeypatch, transport)` | `@databases`, `@pytest.mark.usefixtures('deployed_agent_skill_release')`, `@pytest.mark.parametrize('transport', ['rest', 'mcp'])` | — |
