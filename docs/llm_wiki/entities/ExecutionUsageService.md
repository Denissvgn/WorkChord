# ExecutionUsageService

**Location:** `backend/app/services/execution_usage_service.py:50`
**Kind:** Class
**Bases:** —
**Module:** [execution_usage_service](../modules/execution_usage_service.md)

## Description

_Auto-generated from `ExecutionUsageService` in `backend/app/services/execution_usage_service.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db)` | — | — |
| `response` | `(row)` | `@staticmethod` | — |
| `_run` | *(async)* `(actor, run_id, *, writing = False)` | — | — |
| `_scope` | `(row)` | — | — |
| `_history` | *(async)* `(identity)` | — | — |
| `latest` | *(async)* `(actor, run_id)` | — | — |
| `write` | *(async)* `(actor, run_id, data: ExecutionUsageWrite)` | `@atomic_command` | — |
| `summary` | *(async)* `(*, project_id = None, iteration_id = None, lookback_days = 30, budget_amount = None, budget_currency = None, backlog = False, all_projects = False, all_projects_backlog = False)` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ExecutionUsageService (backend/app/services/execution_usage_service.py)"]
    n1["get_execution_usage (backend/app/mcp_agent_tools.py)"]
    n2["get_execution_usage_summary (backend/app/mcp_agent_tools.py)"]
    n3["record_execution_usage (backend/app/mcp_agent_tools.py)"]
    n4["get_execution_usage (backend/app/routers/agent.py)"]
    n5["record_execution_usage (backend/app/routers/agent.py)"]
    n6["execution_usage_summary (backend/app/routers/task_domain.py)"]
    n7["backend/app/services/agent_run_read_service.py"]
    n8["report_store (backend/tests/test_analytics_scopes.py)"]
    n9["test_deleted_iteration_history_does_not_become_backlog (backend/tests/test_analytics_scopes.py)"]
    n10["test_workspace_reports_keep_authorization_and_recorded_backlog_scope (backend/tests/test_analytics_scopes.py)"]
    n11["test_workspace_reports_preserve_window_and_empty_backlog (backend/tests/test_analytics_scopes.py)"]
    n12["test_concurrent_usage_corrections_reserve_one_head (backend/tests/test_execution_usage.py)"]
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
    click n0 "../modules/execution_usage_service.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/mcp_agent_tools.md"
    click n4 "../modules/routers_agent.md"
    click n5 "../modules/routers_agent.md"
    click n6 "../modules/routers_task_domain.md"
    click n7 "../modules/agent_run_read_service.md"
    click n8 "../modules/test_analytics_scopes.md"
    click n9 "../modules/test_analytics_scopes.md"
    click n10 "../modules/test_analytics_scopes.md"
    click n11 "../modules/test_analytics_scopes.md"
    click n12 "../modules/test_execution_usage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [execution_usage_service](../modules/execution_usage_service.md) | 8 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_execution_usage` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `get_execution_usage_summary` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `record_execution_usage` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `get_execution_usage` | call | [routers_agent](../modules/routers_agent.md) | 1 |
| `record_execution_usage` | call | [routers_agent](../modules/routers_agent.md) | 1 |
| `execution_usage_summary` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `agent_run_read_service` | import | [agent_run_read_service](../modules/agent_run_read_service.md) | — |
| `report_store` | call | [test_analytics_scopes](../modules/test_analytics_scopes.md) | 2 |
| `test_deleted_iteration_history_does_not_become_backlog` | call | [test_analytics_scopes](../modules/test_analytics_scopes.md) | 3 |
| `test_workspace_reports_keep_authorization_and_recorded_backlog_scope` | call | [test_analytics_scopes](../modules/test_analytics_scopes.md) | 1 |
| `test_workspace_reports_preserve_window_and_empty_backlog` | call | [test_analytics_scopes](../modules/test_analytics_scopes.md) | 1 |
| `test_concurrent_usage_corrections_reserve_one_head` | call | [test_execution_usage](../modules/test_execution_usage.md) | 1 |

> References: showing 12 of 18 logical references; 6 omitted by the 12-row generated summary limit.
