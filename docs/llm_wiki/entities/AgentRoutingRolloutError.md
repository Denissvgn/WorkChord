# AgentRoutingRolloutError

**Location:** `backend/app/services/agent_routing_rollout.py:225`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [agent_routing_rollout](../modules/agent_routing_rollout.md)

## Description

Typed guard failure for preview or enforced dispatch.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(code: str, status: AgentRoutingRolloutStatus)` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentRoutingRolloutError (backend/app/services/agent_routing_rollout.py)"]
    n1["RuntimeError"]
    n2["AgentRoutingRolloutService.require_enforced_dispatch (backend/app/services/agent_routing_rollout.py)"]
    n3["AgentRoutingRolloutService.require_preview (backend/app/services/agent_routing_rollout.py)"]
    n4["backend/app/services/agent_routing_service.py"]
    n5["backend/app/services/agent_work_service.py"]
    n6["backend/tests/test_agent_routing_rollout.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/agent_routing_rollout.md"
    click n2 "../modules/agent_routing_rollout.md"
    click n3 "../modules/agent_routing_rollout.md"
    click n4 "../modules/agent_routing_service.md"
    click n5 "../modules/agent_work_service.md"
    click n6 "../modules/test_agent_routing_rollout.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing_rollout](../modules/agent_routing_rollout.md) | 1 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentRoutingRolloutService.require_enforced_dispatch` | call | [agent_routing_rollout](../modules/agent_routing_rollout.md) | 2 |
| `AgentRoutingRolloutService.require_preview` | call | [agent_routing_rollout](../modules/agent_routing_rollout.md) | 1 |
| `agent_routing_service` | import | [agent_routing_service](../modules/agent_routing_service.md) | — |
| `agent_work_service` | import | [agent_work_service](../modules/agent_work_service.md) | — |
| `test_agent_routing_rollout` | import | [test_agent_routing_rollout](../modules/test_agent_routing_rollout.md) | — |
