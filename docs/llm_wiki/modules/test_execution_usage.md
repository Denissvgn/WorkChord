# test_execution_usage Module

**Path:** `backend/tests/test_execution_usage.py`

## Description

Usage provenance, corrections, immutable pricing and permission isolation.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `mcp_agent_tools` |
| `app.commands` | `command_transaction` |
| `app.main` | `app` |
| `app.models.agent` | `AgentActor`, `AgentRun` |
| `app.models.execution_usage` | `ExecutionUsageRecord` |
| `app.schemas.execution_usage` | `ExecutionUsageWrite`, `UsagePricingBasis` |
| `app.services.agent_service` | `AgentConflictError`, `AgentPermissionError` |
| `app.services.execution_usage_service` | `ExecutionUsageService`, `estimate_cost` |
| `app.services.identity_service` | `IdentityService` |
| `app.utils.time` | `utc_now` |
| `asyncio` | `asyncio` |
| `datetime` | `timedelta` |
| `decimal` | `Decimal` |
| `httpx` | `httpx` |
| `pytest` | `pytest` |
| `sqlalchemy` | `func`, `select` |
| `tests.test_delivery_scenarios` | `delivery_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/commands.py"]
    n1["backend/app/main.py"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["backend/app/models/agent.py"]
    n4["backend/app/models/execution_usage.py"]
    n5["backend/app/schemas/execution_usage.py"]
    n6["backend/app/services/agent_service.py"]
    n7["backend/app/services/execution_usage_service.py"]
    n8["backend/app/services/identity_service.py"]
    n9["backend/app/utils/time.py"]
    n10["backend/tests/test_delivery_scenarios.py"]
    n11["backend/tests/test_execution_usage.py"]
    n1 --> n0
    n2 --> n0
    n2 --> n3
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n3 --> n9
    n4 --> n9
    n6 --> n0
    n6 --> n3
    n6 --> n9
    n7 --> n0
    n7 --> n3
    n7 --> n4
    n7 --> n5
    n7 --> n6
    n7 --> n9
    n8 --> n0
    n8 --> n9
    n10 --> n0
    n10 --> n1
    n10 --> n6
    n11 --> n0
    n11 --> n1
    n11 --> n2
    n11 --> n3
    n11 --> n4
    n11 --> n5
    n11 --> n6
    n11 --> n7
    n11 --> n8
    n11 --> n9
    n11 --> n10
    click n0 "../modules/commands.md"
    click n1 "../modules/app_main.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/models_agent.md"
    click n4 "../modules/models_execution_usage.md"
    click n5 "../modules/schemas_execution_usage.md"
    click n6 "../modules/agent_service.md"
    click n7 "../modules/execution_usage_service.md"
    click n8 "../modules/identity_service.md"
    click n9 "../modules/time.md"
    click n10 "../modules/test_delivery_scenarios.md"
    click n11 "../modules/test_execution_usage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [commands](../modules/commands.md) |
| Outbound | [app_main](../modules/app_main.md) |
| Outbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_execution_usage](../modules/models_execution_usage.md) |
| Outbound | [schemas_execution_usage](../modules/schemas_execution_usage.md) |
| Outbound | [agent_service](../modules/agent_service.md) |
| Outbound | [execution_usage_service](../modules/execution_usage_service.md) |
| Outbound | [identity_service](../modules/identity_service.md) |
| Outbound | [time](../modules/time.md) |
| Outbound | [test_delivery_scenarios](../modules/test_delivery_scenarios.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `seed_run` | *(async)* `(factory, scenario)` | — | — |
| `usage` | `(now, **overrides)` | — | — |
| `test_usage_zero_unknown_and_currency_validation` | `()` | — | — |
| `test_usage_replay_correction_and_currency_buckets` | *(async)* `(delivery_store)` | — | — |
| `test_usage_unknown_without_reports_and_foreign_reporter_is_denied` | *(async)* `(delivery_store)` | — | — |
| `test_usage_rest_mcp_parity_and_readonly_human_summary` | *(async)* `(delivery_store)` | — | — |
| `test_reported_zero_and_unknown_are_not_repriced_by_live_metadata` | *(async)* `(delivery_store)` | — | — |
| `test_usage_correction_is_versioned_and_atomic` | *(async)* `(delivery_store)` | — | — |
| `test_concurrent_usage_corrections_reserve_one_head` | *(async)* `(delivery_store)` | — | — |
