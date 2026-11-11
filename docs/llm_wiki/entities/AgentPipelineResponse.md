# AgentPipelineResponse

**Location:** `backend/app/schemas/agent.py:476`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Agent supervision pipeline; every open task appears in exactly one stage.

Stage names and meanings come from ``config/workflow-vocabulary.json``.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `needs_definition` | `list[TaskResponse]` | `needs_definition` | Yes | No | — | — | — | — |
| `ready_to_assign` | `list[TaskResponse]` | `ready_to_assign` | Yes | No | — | — | — | — |
| `assigned_waiting` | `list[TaskResponse]` | `assigned_waiting` | Yes | No | — | — | — | — |
| `start_ready` | `list[TaskResponse]` | `start_ready` | Yes | No | — | — | — | — |
| `executing` | `list[TaskResponse]` | `executing` | Yes | No | — | — | — | — |
| `verification_required` | `list[TaskResponse]` | `verification_required` | Yes | No | — | — | — | — |
| `recovery_required` | `list[TaskResponse]` | `recovery_required` | Yes | No | — | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentPipelineResponse (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["get_agent_pipeline (backend/app/routers/agent.py)"]
    n3["backend/tests/test_workflow_vocabulary.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_agent.md"
    click n2 "../modules/routers_agent.md"
    click n3 "../modules/test_workflow_vocabulary.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 0 | `assigned_waiting`, `executing`, `needs_definition`, `ready_to_assign`, `recovery_required`, `start_ready`, `verification_required` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_agent_pipeline` | call | [routers_agent](../modules/routers_agent.md) | 1 |
| `get_agent_pipeline` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `test_workflow_vocabulary` | import | [test_workflow_vocabulary](../modules/test_workflow_vocabulary.md) | — |
