# AgentRoutingTopologyReadiness

**Location:** `backend/app/services/agent_routing_rollout.py:46`
**Kind:** Class
**Bases:** —
**Module:** [agent_routing_rollout](../modules/agent_routing_rollout.md)

**Decorators:** `@dataclass(frozen=True)`

## Description

Narrow, secret-free input supplied by a server-side topology authority.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `schema_version` | `str` | `TOPOLOGY_READINESS_SCHEMA_VERSION` | — |
| `status` | `AgentRoutingTopologyReadinessStatus` | `AgentRoutingTopologyReadinessStatus.UNAVAILABLE` | — |
| `source` | `AgentRoutingTopologyReadinessSource` | `AgentRoutingTopologyReadinessSource.UNAVAILABLE` | — |
| `topology_id` | `str \| None` | `None` | — |
| `topology_revision` | `int \| None` | `None` | — |
| `blocker_codes` | `tuple[str, ...]` | `('topology_readiness_unavailable',)` | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__post_init__` | `() -> None` | — | — |
| `unavailable` | `() -> 'AgentRoutingTopologyReadiness'` | `@classmethod` | Return the pre-setup fail-closed readiness input. |
| `not_ready` | `(*, topology_id: str, topology_revision: int, blocker_codes: tuple[str, ...]) -> 'AgentRoutingTopologyReadiness'` | `@classmethod` | Return an authoritative but unsatisfied topology input. |
| `ready` | `(*, topology_id: str, topology_revision: int) -> 'AgentRoutingTopologyReadiness'` | `@classmethod` | Return a satisfied topology input from the setup authority. |
| `as_dict` | `() -> dict[str, Any]` | — | Project the bounded input into the public capability status. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentRoutingTopologyReadiness (backend/app/services/agent_routing_rollout.py)"]
    n1["AgentRoutingRolloutService.__init__ (backend/app/services/agent_routing_rollout.py)"]
    n2["AgentRoutingTopologyReadiness.not_ready (backend/app/services/agent_routing_rollout.py)"]
    n3["AgentRoutingTopologyReadiness.ready (backend/app/services/agent_routing_rollout.py)"]
    n4["AgentRoutingTopologyReadiness.unavailable (backend/app/services/agent_routing_rollout.py)"]
    n5["reset_agent_routing_topology_readiness (backend/app/services/agent_routing_rollout.py)"]
    n6["set_agent_routing_topology_readiness (backend/app/services/agent_routing_rollout.py)"]
    n7["AgentTeamSetupService.routing_readiness (backend/app/services/agent_team_setup_service.py)"]
    n8["backend/tests/conftest.py"]
    n9["test_topology_readiness_contract_is_versioned_bounded_and_fail_closed (backend/tests/test_agent_routing_rollout.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/agent_routing_rollout.md"
    click n1 "../modules/agent_routing_rollout.md"
    click n2 "../modules/agent_routing_rollout.md"
    click n3 "../modules/agent_routing_rollout.md"
    click n4 "../modules/agent_routing_rollout.md"
    click n5 "../modules/agent_routing_rollout.md"
    click n6 "../modules/agent_routing_rollout.md"
    click n7 "../modules/agent_team_setup_service.md"
    click n8 "../modules/conftest.md"
    click n9 "../modules/test_agent_routing_rollout.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing_rollout](../modules/agent_routing_rollout.md) | 5 | `blocker_codes`, `schema_version`, `source`, `status`, `topology_id`, `topology_revision` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentRoutingRolloutService.__init__` | type_reference | [agent_routing_rollout](../modules/agent_routing_rollout.md) | — |
| `AgentRoutingTopologyReadiness.not_ready` | call | [agent_routing_rollout](../modules/agent_routing_rollout.md) | 1 |
| `AgentRoutingTopologyReadiness.not_ready` | type_reference | [agent_routing_rollout](../modules/agent_routing_rollout.md) | — |
| `AgentRoutingTopologyReadiness.ready` | call | [agent_routing_rollout](../modules/agent_routing_rollout.md) | 1 |
| `AgentRoutingTopologyReadiness.ready` | type_reference | [agent_routing_rollout](../modules/agent_routing_rollout.md) | — |
| `AgentRoutingTopologyReadiness.unavailable` | call | [agent_routing_rollout](../modules/agent_routing_rollout.md) | 1 |
| `AgentRoutingTopologyReadiness.unavailable` | type_reference | [agent_routing_rollout](../modules/agent_routing_rollout.md) | — |
| `reset_agent_routing_topology_readiness` | type_reference | [agent_routing_rollout](../modules/agent_routing_rollout.md) | — |
| `set_agent_routing_topology_readiness` | type_reference | [agent_routing_rollout](../modules/agent_routing_rollout.md) | — |
| `AgentTeamSetupService.routing_readiness` | type_reference | [agent_team_setup_service](../modules/agent_team_setup_service.md) | — |
| `conftest` | import | [conftest](../modules/conftest.md) | — |
| `test_topology_readiness_contract_is_versioned_bounded_and_fail_closed` | call | [test_agent_routing_rollout](../modules/test_agent_routing_rollout.md) | 1 |

> References: showing 12 of 13 logical references; 1 omitted by the 12-row generated summary limit.
