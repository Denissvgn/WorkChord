# MCPAgentKeyMiddleware

**Location:** `backend/app/mcp_server.py:111`
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
    n3["test_mcp_planning_tools_preview_and_apply_one_receipt (backend/tests/test_capacity_adjustments.py)"]
    n4["test_mcp_tools_preview_apply_and_withdraw_a_transfer (backend/tests/test_capacity_transfers.py)"]
    n5["transport_api (backend/tests/test_delivery_prerequisite_tools.py)"]
    n6["cancel_unconfirmable (backend/tests/test_execution_planning_window.py)"]
    n7["operator_call (backend/tests/test_execution_planning_window.py)"]
    n8["worker_attest (backend/tests/test_execution_planning_window.py)"]
    n9["test_reconciliation_uses_operator_and_archived_catalog (backend/tests/test_execution_reconciliation.py)"]
    n10["test_mcp_http_uses_the_same_principal_and_project_boundary (backend/tests/test_identity_lifecycle.py)"]
    n11["test_mcp_preview_then_update_with_returned_revisions (backend/tests/test_iteration_date_move.py)"]
    n12["AgentProtocol.__aenter__ (backend/tests/test_manual_provenance_record.py)"]
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
    n11 --> n0
    n12 --> n0
    click n0 "../modules/mcp_server.md"
    click n1 "../modules/mcp_server.md"
    click n2 "../modules/test_annual_calendar_work_control.md"
    click n3 "../modules/test_capacity_adjustments.md"
    click n4 "../modules/test_capacity_transfers.md"
    click n5 "../modules/test_delivery_prerequisite_tools.md"
    click n6 "../modules/test_execution_planning_window.md"
    click n7 "../modules/test_execution_planning_window.md"
    click n8 "../modules/test_execution_planning_window.md"
    click n9 "../modules/test_execution_reconciliation.md"
    click n10 "../modules/test_identity_lifecycle.md"
    click n11 "../modules/test_iteration_date_move.md"
    click n12 "../modules/test_manual_provenance_record.md"
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
| `test_mcp_planning_tools_preview_and_apply_one_receipt` | call | [test_capacity_adjustments](../modules/test_capacity_adjustments.md) | 1 |
| `test_mcp_tools_preview_apply_and_withdraw_a_transfer` | call | [test_capacity_transfers](../modules/test_capacity_transfers.md) | 1 |
| `transport_api` | call | [test_delivery_prerequisite_tools](../modules/test_delivery_prerequisite_tools.md) | 1 |
| `cancel_unconfirmable` | call | [test_execution_planning_window](../modules/test_execution_planning_window.md) | 1 |
| `operator_call` | call | [test_execution_planning_window](../modules/test_execution_planning_window.md) | 1 |
| `worker_attest` | call | [test_execution_planning_window](../modules/test_execution_planning_window.md) | 1 |
| `test_reconciliation_uses_operator_and_archived_catalog` | call | [test_execution_reconciliation](../modules/test_execution_reconciliation.md) | 2 |
| `test_mcp_http_uses_the_same_principal_and_project_boundary` | call | [test_identity_lifecycle](../modules/test_identity_lifecycle.md) | 1 |
| `test_mcp_preview_then_update_with_returned_revisions` | call | [test_iteration_date_move](../modules/test_iteration_date_move.md) | 1 |
| `AgentProtocol.__aenter__` | call | [test_manual_provenance_record](../modules/test_manual_provenance_record.md) | 1 |

> References: showing 12 of 20 logical references; 8 omitted by the 12-row generated summary limit.
