# TaskRoutingAssessmentCreate

**Location:** `backend/app/schemas/agent_routing.py:606`
**Kind:** Pydantic model
**Bases:** `TaskRoutingAssessmentFields`
**Module:** [agent_routing](../modules/agent_routing.md)

## Description

Create payload for one append-only assessment.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskRoutingAssessmentCreate (backend/app/schemas/agent_routing.py)"]
    n1["TaskRoutingAssessmentFields (backend/app/schemas/agent_routing.py)"]
    n2["AgentRoutingService.create_assessment (backend/app/services/agent_routing_service.py)"]
    n3["backend/tests/test_agent_routing_contract.py"]
    n4["backend/tests/test_agent_routing_data.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/agent_routing.md"
    click n1 "../modules/agent_routing.md"
    click n2 "../modules/agent_routing_service.md"
    click n3 "../modules/test_agent_routing_contract.md"
    click n4 "../modules/test_agent_routing_data.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing](../modules/agent_routing.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `TaskRoutingAssessmentFields` | [agent_routing](../modules/agent_routing.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentRoutingService.create_assessment` | call | [agent_routing_service](../modules/agent_routing_service.md) | 1 |
| `test_agent_routing_contract` | import | [test_agent_routing_contract](../modules/test_agent_routing_contract.md) | — |
| `test_agent_routing_data` | import | [test_agent_routing_data](../modules/test_agent_routing_data.md) | — |
