# MCPAgentKeyMiddleware

**Location:** `backend/app/mcp_server.py:110`
**Kind:** Class
**Bases:** —
**Module:** [mcp_server](../modules/mcp_server.md)

## Description

Extract and validate MCP HTTP agent credentials before protocol handling.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(app: ASGIApp)` | — | — |
| `__call__` | *(async)* `(scope: Scope, receive: Receive, send: Send) -> None` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MCPAgentKeyMiddleware (backend/app/mcp_server.py)"]
    n1["create_mcp_http_app (backend/app/mcp_server.py)"]
    n2["calendar_edit (backend/tests/test_annual_calendar_work_control.py)"]
    n3["cancel_unconfirmable (backend/tests/test_execution_planning_window.py)"]
    n4["operator_call (backend/tests/test_execution_planning_window.py)"]
    n5["worker_attest (backend/tests/test_execution_planning_window.py)"]
    n6["test_reconciliation_uses_operator_and_archived_catalog (backend/tests/test_execution_reconciliation.py)"]
    n7["test_mcp_http_uses_the_same_principal_and_project_boundary (backend/tests/test_identity_lifecycle.py)"]
    n8["test_scoped_single_year_forecast (backend/tests/test_pm_forecast_calendar.py)"]
    n9["assignment_api (backend/tests/test_team_pm_dispatch.py)"]
    n10["recovery_api (backend/tests/test_team_pm_recovery.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    click n0 "../modules/mcp_server.md"
    click n1 "../modules/mcp_server.md"
    click n2 "../modules/test_annual_calendar_work_control.md"
    click n3 "../modules/test_execution_planning_window.md"
    click n4 "../modules/test_execution_planning_window.md"
    click n5 "../modules/test_execution_planning_window.md"
    click n6 "../modules/test_execution_reconciliation.md"
    click n7 "../modules/test_identity_lifecycle.md"
    click n8 "../modules/test_pm_forecast_calendar.md"
    click n9 "../modules/test_team_pm_dispatch.md"
    click n10 "../modules/test_team_pm_recovery.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [mcp_server](../modules/mcp_server.md) | 2 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_mcp_http_app` | call | [mcp_server](../modules/mcp_server.md) | 1 |
| `calendar_edit` | call | [test_annual_calendar_work_control](../modules/test_annual_calendar_work_control.md) | 1 |
| `cancel_unconfirmable` | call | [test_execution_planning_window](../modules/test_execution_planning_window.md) | 1 |
| `operator_call` | call | [test_execution_planning_window](../modules/test_execution_planning_window.md) | 1 |
| `worker_attest` | call | [test_execution_planning_window](../modules/test_execution_planning_window.md) | 1 |
| `test_reconciliation_uses_operator_and_archived_catalog` | call | [test_execution_reconciliation](../modules/test_execution_reconciliation.md) | 2 |
| `test_mcp_http_uses_the_same_principal_and_project_boundary` | call | [test_identity_lifecycle](../modules/test_identity_lifecycle.md) | 1 |
| `test_scoped_single_year_forecast` | call | [test_pm_forecast_calendar](../modules/test_pm_forecast_calendar.md) | 1 |
| `assignment_api` | call | [test_team_pm_dispatch](../modules/test_team_pm_dispatch.md) | 1 |
| `recovery_api` | call | [test_team_pm_recovery](../modules/test_team_pm_recovery.md) | 1 |
