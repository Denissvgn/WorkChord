# AgentConnectModel

**Location:** `backend/app/schemas/agent_connect.py:9`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent_connect](../modules/schemas_agent_connect.md)

## Description

Reject undeclared fields so nothing extra is ever published here.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Attributes

*No annotated attributes found.*

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentConnectModel (backend/app/schemas/agent_connect.py)"]
    n1["BaseModel"]
    n2["AgentConnectCredential (backend/app/schemas/agent_connect.py)"]
    n3["AgentConnectResponse (backend/app/schemas/agent_connect.py)"]
    n4["AgentConnectRole (backend/app/schemas/agent_connect.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_agent_connect.md"
    click n2 "../modules/schemas_agent_connect.md"
    click n3 "../modules/schemas_agent_connect.md"
    click n4 "../modules/schemas_agent_connect.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent_connect](../modules/schemas_agent_connect.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
| Subclass | `AgentConnectCredential` | [schemas_agent_connect](../modules/schemas_agent_connect.md) |
| Subclass | `AgentConnectResponse` | [schemas_agent_connect](../modules/schemas_agent_connect.md) |
| Subclass | `AgentConnectRole` | [schemas_agent_connect](../modules/schemas_agent_connect.md) |
