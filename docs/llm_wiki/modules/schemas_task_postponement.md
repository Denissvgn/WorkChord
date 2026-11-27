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
    n0["backend/app/routers/task_domain.py"]
    n1["backend/app/schemas/task.py"]
    n2["backend/app/schemas/task_detail.py"]
    n3["backend/app/schemas/task_postponement.py"]
    n4["backend/tests/test_task_postponement.py"]
    n5["backend/tests/test_task_reactivation.py"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n2 --> n1
    n2 --> n3
    n3 --> n1
    n4 --> n1
    n4 --> n3
    n5 --> n1
    n5 --> n3
    n5 --> n4
    click n0 "../modules/routers_task_domain.md"
    click n1 "../modules/schemas_task.md"
    click n2 "../modules/task_detail.md"
    click n3 "../modules/schemas_task_postponement.md"
    click n4 "../modules/test_task_postponement.md"
    click n5 "../modules/test_task_reactivation.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_task_domain](../modules/routers_task_domain.md) |
| Inbound | [task_detail](../modules/task_detail.md) |
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
| [TaskPostponementResponse](../entities/schemas_task_postponement_TaskPostponementResponse.md) | Pydantic model | 157 | `BaseModel` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_stripped` | `(value: str \| None) -> str \| None` | — | — |
