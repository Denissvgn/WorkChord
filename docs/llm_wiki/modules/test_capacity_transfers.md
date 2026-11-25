# test_capacity_transfers Module

**Path:** `backend/tests/test_capacity_transfers.py`

## Description

A temporary capacity transfer lends availability between rows of one person and returns it after its dates.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `mcp_server` |
| `app.config` | `get_settings` |
| `app.models.agent` | `AgentTaskAssignment` |
| `app.models.calendar` | `Calendar` |
| `app.models.identity` | `CommandAudit`, `ProjectMembership`, `WorkspaceMembership` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMemberCapacityAdjustment`, `TeamMember` |
| `app.services` | `capacity_transfers` |
| `app.services.agent_service` | `hash_api_key` |
| `app.services.capacity_adjustments` | `load_dated_availability` |
| `app.services.identity_service` | `IdentityService` |
| `datetime` | `date` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `func`, `select`, `update` |
| `tests.test_capacity_adjustments` | `client`, `headers`, `managed` |
| `tests.test_iteration_date_move` | `human` |
| `tests.test_review_provenance` | `database_engines` |
| `tests.test_team_pm_dispatch` | `db_session_factory` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_capacity_transfers.py"]
    n1 --> n0
    click n1 "../modules/test_capacity_transfers.md"
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
| `restore_settings_cache` | `()` | `@pytest.fixture(autouse=True)` | — |
| `shared_agent` | *(async)* `(db, profile_factory, team_member_factory)` | — | One person holds a quarter of each day in Pi and in each of three lending projects. |
| `lend` | `(rows, percent = 10, start = START, end = END, **extra)` | — | — |
| `percents` | *(async)* `(factory, rows, days = (BEFORE, START, MIDDLE, END, AFTER))` | — | Each row's effective percentage on each date, as every capacity calculation reads it. |
| `revisions` | *(async)* `(factory)` | — | — |
| `test_lending_from_three_projects_to_pi_returns_after_the_window` | *(async)* `(db_session, db_session_factory, profile_factory, team_member_factory, actor_factory, monkeypatch)` | `@database_engines` | — |
| `test_lending_under_issued_work_is_refused_and_withdrawing_under_target_work_too` | *(async)* `(db_session, db_session_factory, profile_factory, team_member_factory, actor_factory, monkeypatch)` | `@database_engines` | — |
| `test_returning_a_started_transfer_keeps_its_elapsed_dates` | *(async)* `(db_session, db_session_factory, profile_factory, team_member_factory, monkeypatch)` | `@database_engines` | — |
| `test_transfer_needs_edit_access_to_every_row_and_does_not_reveal_others` | *(async)* `(db_session, db_session_factory, profile_factory, team_member_factory, monkeypatch)` | `@database_engines` | — |
| `test_mcp_tools_preview_apply_and_withdraw_a_transfer` | *(async)* `(db_session, db_session_factory, profile_factory, team_member_factory, actor_factory, monkeypatch)` | `@database_engines` | — |
