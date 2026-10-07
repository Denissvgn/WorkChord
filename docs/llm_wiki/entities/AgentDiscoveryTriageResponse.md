# AgentDiscoveryTriageResponse

**Location:** `backend/app/schemas/agent.py:1138`
**Kind:** Pydantic model
**Bases:** `TriageItemResponse`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Created discovery Triage item with source linkage metadata.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentDiscoveryTriageResponse (backend/app/schemas/agent.py)"]
    n1["TriageItemResponse (backend/app/schemas/triage.py)"]
    n2["report_agent_discovery (backend/app/routers/agent.py)"]
    n3["AgentWorkService.report_discovery (backend/app/services/agent_work_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_agent.md"
    click n1 "../modules/schemas_triage.md"
    click n2 "../modules/routers_agent.md"
    click n3 "../modules/agent_work_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `TriageItemResponse` | [schemas_triage](../modules/schemas_triage.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `report_agent_discovery` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentWorkService.report_discovery` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
