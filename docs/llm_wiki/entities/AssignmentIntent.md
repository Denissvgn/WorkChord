# AssignmentIntent

**Location:** `backend/app/services/agent_routing_policy.py:177`
**Kind:** Enum
**Bases:** `StrEnum`
**Module:** [agent_routing_policy](../modules/agent_routing_policy.md)

## Description

Normalized assignment intents derived from purpose and queue class.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `EXECUTION` | `'execution'` | — |
| `VERIFICATION` | `'verification'` | — |
| `REWORK` | `'rework'` | — |
| `RECOVERY` | `'recovery'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AssignmentIntent (backend/app/services/agent_routing_policy.py)"]
    n1["StrEnum"]
    n2["evaluate_actor_authorization (backend/app/services/agent_routing_policy.py)"]
    n3["evaluate_assignment_compatibility (backend/app/services/agent_routing_policy.py)"]
    n4["test_execution_intents_share_capacity_profile_rules (backend/tests/test_agent_routing_contract.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/agent_routing_policy.md"
    click n2 "../modules/agent_routing_policy.md"
    click n3 "../modules/agent_routing_policy.md"
    click n4 "../modules/test_agent_routing_contract.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing_policy](../modules/agent_routing_policy.md) | 0 | `EXECUTION`, `RECOVERY`, `REWORK`, `VERIFICATION` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrEnum` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `evaluate_actor_authorization` | call | [agent_routing_policy](../modules/agent_routing_policy.md) | 1 |
| `evaluate_assignment_compatibility` | call | [agent_routing_policy](../modules/agent_routing_policy.md) | 1 |
| `test_execution_intents_share_capacity_profile_rules` | type_reference | [test_agent_routing_contract](../modules/test_agent_routing_contract.md) | — |
