# test_run_detail_execution_provenance Module

**Path:** `backend/tests/test_run_detail_execution_provenance.py`

## Description

Run detail returns the stored execution provenance through REST and MCP alike.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `mcp_agent_tools` |
| `app.main` | `app` |
| `app.models.agent` | `AgentActor`, `AgentRun` |
| `app.utils.time` | `utc_now` |
| `datetime` | `timedelta` |
| `httpx` | `httpx` |
| `pytest` | `pytest` |
| `tests.test_delivery_scenarios` | `delivery_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/main.py"]
    n1["backend/app/mcp_agent_tools.py"]
    n2["backend/app/models/agent.py"]
    n3["backend/app/utils/time.py"]
    n4["backend/tests/test_delivery_scenarios.py"]
    n5["backend/tests/test_run_detail_execution_provenance.py"]
    n1 --> n2
    n2 --> n3
    n4 --> n0
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n4
    click n0 "../modules/app_main.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/models_agent.md"
    click n3 "../modules/time.md"
    click n4 "../modules/test_delivery_scenarios.md"
    click n5 "../modules/test_run_detail_execution_provenance.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [app_main](../modules/app_main.md) |
| Outbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [time](../modules/time.md) |
| Outbound | [test_delivery_scenarios](../modules/test_delivery_scenarios.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `fresh_provenance` | `(actor_id)` | — | — |
| `reconciled_provenance` | `(actor_id)` | — | — |
| `test_run_detail_rest_and_mcp_return_the_same_stored_provenance` | *(async)* `(delivery_store, build)` | `@pytest.mark.parametrize('build', [fresh_provenance, reconciled_provenance], ids=['fresh', 'reconciled'])` | — |
