# task_postponement Module

**Path:** `backend/app/schemas/task_postponement.py`

## Description

Postpone and reactivate commands and the postponement record they return.

## Imports

| Source | Symbols |
|--------|---------|
| `app.schemas.task` | `TaskResponse` |
| `datetime` | `date`, `datetime` |
| `pydantic` | `BaseModel`, `ConfigDict`, `Field`, `field_validator`, `model_validator` |
| `typing` | `Literal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_agent_tools.py"]
    n1["backend/app/routers/task_domain.py"]
    n2["backend/app/schemas/task.py"]
    n3["backend/app/schemas/task_detail.py"]
    n4["backend/app/schemas/task_postponement.py"]
    n5["backend/app/services/agent_planning_service.py"]
    n6["backend/tests/test_task_postponement.py"]
    n7["backend/tests/test_task_reactivation.py"]
    n0 --> n2
    n0 --> n4
    n0 --> n5
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n3 --> n2
    n3 --> n4
    n4 --> n2
    n5 --> n2
    n5 --> n4
    n6 --> n2
    n6 --> n4
    n7 --> n2
    n7 --> n4
    n7 --> n6
    click n0 "../modules/mcp_agent_tools.md"
    click n1 "../modules/routers_task_domain.md"
    click n2 "../modules/schemas_task.md"
    click n3 "../modules/task_detail.md"
    click n4 "../modules/schemas_task_postponement.md"
    click n5 "../modules/agent_planning_service.md"
    click n6 "../modules/test_task_postponement.md"
    click n7 "../modules/test_task_reactivation.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [routers_task_domain](../modules/routers_task_domain.md) |
| Inbound | [task_detail](../modules/task_detail.md) |
| Inbound | [agent_planning_service](../modules/agent_planning_service.md) |
| Inbound | [test_task_postponement](../modules/test_task_postponement.md) |
| Inbound | [test_task_reactivation](../modules/test_task_reactivation.md) |
| Outbound | [schemas_task](../modules/schemas_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [RequirementKind](../entities/RequirementKind.md) | Type alias | 10 | `Literal['predecessor_accepted', 'date', 'owner_decision', 'linked_resolved']` | — |
| [ReactivationRequirementInput](../entities/schemas_task_postponement_ReactivationRequirementInput.md) | Pydantic model | 24 | `BaseModel` | One condition that must hold before postponed work resumes. |
| [TaskPostponeRequest](../entities/TaskPostponeRequest.md) | Pydantic model | 60 | `BaseModel` | Stop planned, active or resolved work until its reactivation requirements are met. |
| [TaskReactivateRequest](../entities/TaskReactivateRequest.md) | Pydantic model | 83 | `BaseModel` | Return postponed work to planned, or to resolved when it was postponed after resolution. |
| [OwnerDecisionRequest](../entities/OwnerDecisionRequest.md) | Pydantic model | 97 | `BaseModel` | Record that the owner made the decision an owner_decision requirement waits for. |
| [ReactivationRequirementResponse](../entities/ReactivationRequirementResponse.md) | Pydantic model | 115 | `BaseModel` | — |
| [PostponementRelease](../entities/PostponementRelease.md) | Pydantic model | 127 | `BaseModel` | Execution ownership the postponement ended through the fenced release. |
| [TaskPostponementRecord](../entities/schemas_task_postponement_TaskPostponementRecord.md) | Pydantic model | 136 | `BaseModel` | — |
| [TaskPostponementResponse](../entities/schemas_task_postponement_TaskPostponementResponse.md) | Pydantic model | 158 | `BaseModel` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_stripped` | `(value: str \| None) -> str \| None` | — | — |
