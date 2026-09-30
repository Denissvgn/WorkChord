# AgentRoutingRolloutService

**Location:** `backend/app/services/agent_routing_rollout.py:234`
**Kind:** Class
**Bases:** —
**Module:** [agent_routing_rollout](../modules/agent_routing_rollout.md)

## Description

Resolve deployment mode against authoritative topology readiness.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(*, settings_override: Any \| None = None, topology_readiness: AgentRoutingTopologyReadiness \| None = None)` | — | — |
| `status` | `() -> AgentRoutingRolloutStatus` | — | Return the effective mode, failing closed until topology is ready. |
| `require_preview` | `() -> AgentRoutingRolloutStatus` | — | Permit model-aware previews only in effective shadow/enforced modes. |
| `require_enforced_dispatch` | `() -> AgentRoutingRolloutStatus` | — | Permit enforced dispatch only in the effective enforced mode. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentRoutingRolloutService (backend/app/services/agent_routing_rollout.py)"]
    n1["get_agent_capabilities (backend/app/mcp_agent_tools.py)"]
    n2["get_agent_capabilities (backend/app/routers/agent.py)"]
    n3["AgentRoutingService.__init__ (backend/app/services/agent_routing_service.py)"]
    n4["AgentRoutingService._require_preview_rollout (backend/app/services/agent_routing_service.py)"]
    n5["AgentWorkService.__init__ (backend/app/services/agent_work_service.py)"]
    n6["AgentWorkService._require_enforced_rollout (backend/app/services/agent_work_service.py)"]
    n7["AgentWorkService._require_supervised_rollout (backend/app/services/agent_work_service.py)"]
    n8["AgentWorkService._resolve_rollout (backend/app/services/agent_work_service.py)"]
    n9["test_feature_off_rollback_preserves_representative_routing_history (backend/tests/test_agent_routing_rollout.py)"]
    n10["test_inactive_rollout_blocks_queued_model_aware_verification_review (backend/tests/test_agent_routing_rollout.py)"]
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
    click n0 "../modules/agent_routing_rollout.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/routers_agent.md"
    click n3 "../modules/agent_routing_service.md"
    click n4 "../modules/agent_routing_service.md"
    click n5 "../modules/agent_work_service.md"
    click n6 "../modules/agent_work_service.md"
    click n7 "../modules/agent_work_service.md"
    click n8 "../modules/agent_work_service.md"
    click n9 "../modules/test_agent_routing_rollout.md"
    click n10 "../modules/test_agent_routing_rollout.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing_rollout](../modules/agent_routing_rollout.md) | 4 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_agent_capabilities` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 3 |
| `get_agent_capabilities` | call | [routers_agent](../modules/routers_agent.md) | 3 |
| `AgentRoutingService.__init__` | type_reference | [agent_routing_service](../modules/agent_routing_service.md) | — |
| `AgentRoutingService._require_preview_rollout` | call | [agent_routing_service](../modules/agent_routing_service.md) | 3 |
| `AgentWorkService.__init__` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService.__init__` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `AgentWorkService._require_enforced_rollout` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `AgentWorkService._require_supervised_rollout` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `AgentWorkService._resolve_rollout` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService._resolve_rollout` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `test_feature_off_rollback_preserves_representative_routing_history` | call | [test_agent_routing_rollout](../modules/test_agent_routing_rollout.md) | 2 |
| `test_inactive_rollout_blocks_queued_model_aware_verification_review` | call | [test_agent_routing_rollout](../modules/test_agent_routing_rollout.md) | 1 |

> References: showing 12 of 19 logical references; 7 omitted by the 12-row generated summary limit.
