# test_annual_calendar_work_control Module

**Path:** `backend/tests/test_annual_calendar_work_control.py`

## Description

Annual planning inputs and execution authority are independently fenced.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `mcp_server` |
| `app.config` | `get_settings` |
| `app.main` | `app` |
| `app.models.agent` | `AgentModelCatalogEntry`, `AgentRun`, `AgentTaskAssignment` |
| `app.models.calendar` | `Calendar` |
| `app.models.identity` | `ProjectMembership`, `WorkspaceMembership` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.services.identity_service` | `IdentityService`, `initialize_control_plane` |
| `app.services.iteration_service` | `IterationService` |
| `datetime` | `date` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `select` |
| `tests` | `test_team_pm_dispatch` |
| `tests.test_agent_team_setup_qualification` | `provision_ready_topology`, `routing_base` |
| `tests.test_execution_planning_window` | `planning_patch` |
| `tests.test_review_provenance_transports` | `databases`, `fence` |
| `tests.test_team_pm_recovery` | `recovery_api` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_annual_calendar_work_control.py"]
    n1 --> n0
    click n1 "../modules/test_annual_calendar_work_control.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (16) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 16 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `pm_headers` | `(key, receipt)` | — | — |
| `apply_inputs` | `(receipt)` | — | — |
| `calendar_edit` | *(async)* `(http, transport, key, iteration, revision, label, *, refused = False, **changes)` | — | — |
| `test_annual_selection_and_forecast_preserve_live_ownership` | *(async)* `(db_session, db_session_factory, team_member_factory, task_factory, monkeypatch, transport, lane)` | `@databases`, `@pytest.mark.parametrize('transport', ['rest', 'mcp'])`, `@pytest.mark.parametrize('lane', ['running', 'verification', 'rework'])`, `@pytest.mark.usefixtures('deployed_agent_skill_release')` | — |
| `test_mcp_reports_an_existing_issued_year_conflict` | *(async)* `(db_session, db_session_factory, team_member_factory, task_factory, monkeypatch, record_property)` | `@databases`, `@pytest.mark.usefixtures('deployed_agent_skill_release')` | Real team dispatch and an already protected supplemental-year removal exercise the error adapter. |
