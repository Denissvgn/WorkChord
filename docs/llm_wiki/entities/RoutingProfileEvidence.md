# RoutingProfileEvidence

**Location:** `backend/app/services/agent_routing_policy.py:528`
**Kind:** Class
**Bases:** —
**Module:** [agent_routing_policy](../modules/agent_routing_policy.md)

**Decorators:** `@dataclass(frozen=True)`

## Description

Secret-free profile evidence used by compatibility decisions.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `profile_id` | `int` | *required* | — |
| `profile_kind` | `str` | *required* | — |
| `automation_enabled` | `bool` | *required* | — |
| `assignment_modes` | `frozenset[str]` | `field(default_factory=frozenset)` | — |
| `skill_levels` | `Mapping[str, int]` | `field(default_factory=dict)` | — |
| `weakness_keys` | `frozenset[str]` | `field(default_factory=frozenset)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RoutingProfileEvidence (backend/app/services/agent_routing_policy.py)"]
    n1["evaluate_assignment_compatibility (backend/app/services/agent_routing_policy.py)"]
    n2["AgentRoutingService._profile_evidence (backend/app/services/agent_routing_service.py)"]
    n3["_profile (backend/tests/test_agent_routing_contract.py)"]
    n4["test_profile_and_capacity_compatibility_blockers (backend/tests/test_agent_routing_contract.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/agent_routing_policy.md"
    click n1 "../modules/agent_routing_policy.md"
    click n2 "../modules/agent_routing_service.md"
    click n3 "../modules/test_agent_routing_contract.md"
    click n4 "../modules/test_agent_routing_contract.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing_policy](../modules/agent_routing_policy.md) | 0 | `assignment_modes`, `automation_enabled`, `profile_id`, `profile_kind`, `skill_levels`, `weakness_keys` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `evaluate_assignment_compatibility` | type_reference | [agent_routing_policy](../modules/agent_routing_policy.md) | — |
| `AgentRoutingService._profile_evidence` | call | [agent_routing_service](../modules/agent_routing_service.md) | 1 |
| `AgentRoutingService._profile_evidence` | type_reference | [agent_routing_service](../modules/agent_routing_service.md) | — |
| `_profile` | call | [test_agent_routing_contract](../modules/test_agent_routing_contract.md) | 1 |
| `_profile` | type_reference | [test_agent_routing_contract](../modules/test_agent_routing_contract.md) | — |
| `test_profile_and_capacity_compatibility_blockers` | type_reference | [test_agent_routing_contract](../modules/test_agent_routing_contract.md) | — |
