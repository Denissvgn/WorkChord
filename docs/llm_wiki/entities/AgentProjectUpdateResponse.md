# AgentProjectUpdateResponse

**Location:** `backend/app/schemas/agent.py:1087`
**Kind:** Pydantic model
**Bases:** `ProjectUpdateEntryResponse`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Agent project-update response with attribution and evidence.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentProjectUpdateResponse (backend/app/schemas/agent.py)"]
    n1["ProjectUpdateEntryResponse (backend/app/schemas/project.py)"]
    n2["create_agent_project_update (backend/app/routers/agent.py)"]
    n3["AgentWorkService.create_project_update (backend/app/services/agent_work_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_agent.md"
    click n1 "../modules/schemas_project.md"
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
| Base | `ProjectUpdateEntryResponse` | [schemas_project](../modules/schemas_project.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_agent_project_update` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentWorkService.create_project_update` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
