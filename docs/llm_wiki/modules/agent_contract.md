# agent_contract Module

**Path:** `backend/app/agent_contract.py`

## Description

Shared capability handshake contract for REST and MCP projections.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/agent_contract.py"]
    n1["backend/app/mcp_agent_tools.py"]
    n2["backend/app/routers/agent.py"]
    n3["backend/app/services/agent_team_setup_service.py"]
    n4["backend/tests/test_agent_model_catalog_api.py"]
    n5["backend/tests/test_agent_routing_rollout.py"]
    n6["backend/tests/test_agent_skill_routing_guidance.py"]
    n7["scripts/ci/check_model_aware_routing_closeout.py"]
    n1 --> n0
    n1 --> n3
    n2 --> n0
    n2 --> n3
    n3 --> n0
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n7 --> n0
    click n0 "../modules/agent_contract.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/routers_agent.md"
    click n3 "../modules/agent_team_setup_service.md"
    click n4 "../modules/test_agent_model_catalog_api.md"
    click n5 "../modules/test_agent_routing_rollout.md"
    click n6 "../modules/test_agent_skill_routing_guidance.md"
    click n7 "../modules/check_model_aware_routing_closeout.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [routers_agent](../modules/routers_agent.md) |
| Inbound | [agent_team_setup_service](../modules/agent_team_setup_service.md) |
| Inbound | [test_agent_model_catalog_api](../modules/test_agent_model_catalog_api.md) |
| Inbound | [test_agent_routing_rollout](../modules/test_agent_routing_rollout.md) |
| Inbound | [test_agent_skill_routing_guidance](../modules/test_agent_skill_routing_guidance.md) |
| Inbound | [check_model_aware_routing_closeout](../modules/check_model_aware_routing_closeout.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `agent_contract_features` | `(*, include_skill_bundles: bool, model_aware_routing_mode: str = 'off') -> list[str]` | — | Return one ordered feature projection shared by REST and MCP. |
