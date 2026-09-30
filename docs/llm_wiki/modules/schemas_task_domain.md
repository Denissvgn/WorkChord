# task_domain Module

**Path:** `backend/app/schemas/task_domain.py`

## Description

Explicit task commands and typed action availability.

## Imports

| Source | Symbols |
|--------|---------|
| `pydantic` | `BaseModel`, `ConfigDict`, `Field`, `model_validator` |
| `typing` | `Literal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_agent_tools.py"]
    n1["backend/app/routers/task_domain.py"]
    n2["backend/app/schemas/task_domain.py"]
    n3["backend/app/services/task_domain_service.py"]
    n4["backend/tests/test_delivery_dependencies.py"]
    n5["backend/tests/test_task_domain.py"]
    n6["backend/tests/test_task_domain_integrity.py"]
    n0 --> n2
    n0 --> n3
    n1 --> n2
    n1 --> n3
    n3 --> n2
    n4 --> n2
    n4 --> n3
    n5 --> n0
    n5 --> n2
    n5 --> n3
    n6 --> n2
    n6 --> n3
    n6 --> n5
    click n0 "../modules/mcp_agent_tools.md"
    click n1 "../modules/routers_task_domain.md"
    click n2 "../modules/schemas_task_domain.md"
    click n3 "../modules/task_domain_service.md"
    click n4 "../modules/test_delivery_dependencies.md"
    click n5 "../modules/test_task_domain.md"
    click n6 "../modules/test_task_domain_integrity.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [routers_task_domain](../modules/routers_task_domain.md) |
| Inbound | [task_domain_service](../modules/task_domain_service.md) |
| Inbound | [test_delivery_dependencies](../modules/test_delivery_dependencies.md) |
| Inbound | [test_task_domain](../modules/test_task_domain.md) |
| Inbound | [test_task_domain_integrity](../modules/test_task_domain_integrity.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskAction](../entities/TaskAction.md) | Type alias | 7 | `Literal['start_manual', 'resolve_manual', 'block', 'unblock', 'cancel', 'reopen', 'commit', 'uncommit']` | — |
| [TaskActionRequest](../entities/TaskActionRequest.md) | Pydantic model | 10 | `BaseModel` | — |
| [TaskActionBlocker](../entities/TaskActionBlocker.md) | Pydantic model | 30 | `BaseModel` | — |
| [TaskActionAvailability](../entities/schemas_task_domain_TaskActionAvailability.md) | Pydantic model | 35 | `BaseModel` | — |
| [TaskActionsResponse](../entities/TaskActionsResponse.md) | Pydantic model | 41 | `BaseModel` | — |
| [BacklogRestoreRequest](../entities/BacklogRestoreRequest.md) | Pydantic model | 50 | `BaseModel` | — |
