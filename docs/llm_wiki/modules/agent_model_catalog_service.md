# agent_model_catalog_service Module

**Path:** `backend/app/services/agent_model_catalog_service.py`

## Description

Operator-owned model catalog, binding administration, and audit receipts.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.models.agent` | `AgentActor`, `AgentIdempotencyRecord`, `AgentModelBinding`, `AgentModelCatalogEntry`, `AgentRun`, `AgentTaskAssignment`, `TaskEvent` |
| `app.query_limits` | `CollectionLimitExceededError`, `MAX_BOUNDED_LIST_ITEMS` |
| `app.schemas.agent_planning` | `AgentPlanningCommandContext` |
| `app.schemas.agent_routing` | `AgentModelBindingCreate`, `AgentModelBindingDisable`, `AgentModelBindingResponse`, `AgentModelBindingUpdate`, `AgentModelCatalogCreate`, `AgentModelCatalogDisable`, `AgentModelCatalogResponse`, `AgentModelCatalogUpdate`, `AgentModelMutationReceipt` |
| `app.services.agent_service` | `AgentConflictError`, `AgentPermissionError`, `actor_has_scope`, `require_scope`, `validate_idempotency_key` |
| `collections.abc` | `Awaitable`, `Callable` |
| `dataclasses` | `dataclass` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `secrets` | `secrets` |
| `sqlalchemy` | `func`, `select`, `text` |
| `sqlalchemy.exc` | `IntegrityError` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `sqlalchemy.orm` | `selectinload` |
| `typing` | `Any`, `Literal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_agent_tools.py"]
    n1["backend/app/mcp_server.py"]
    n2["backend/app/models/agent.py"]
    n3["backend/app/query_limits.py"]
    n4["backend/app/routers/agent_catalog.py"]
    n5["backend/app/schemas/agent_planning.py"]
    n6["backend/app/schemas/agent_routing.py"]
    n7["backend/app/services/agent_model_catalog_service.py"]
    n8["backend/app/services/agent_service.py"]
    n9["backend/app/services/agent_work_service.py"]
    n10["backend/tests/test_agent_model_catalog_api.py"]
    n0 --> n2
    n0 --> n5
    n0 --> n6
    n0 --> n7
    n0 --> n8
    n0 --> n9
    n1 --> n0
    n1 --> n2
    n1 --> n7
    n1 --> n8
    n4 --> n2
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n7 --> n2
    n7 --> n3
    n7 --> n5
    n7 --> n6
    n7 --> n8
    n8 --> n2
    n8 --> n3
    n9 --> n2
    n9 --> n3
    n9 --> n5
    n9 --> n7
    n9 --> n8
    n10 --> n0
    n10 --> n1
    n10 --> n2
    n10 --> n5
    n10 --> n6
    n10 --> n7
    n10 --> n8
    n10 --> n9
    click n0 "../modules/mcp_agent_tools.md"
    click n1 "../modules/mcp_server.md"
    click n2 "../modules/models_agent.md"
    click n3 "../modules/query_limits.md"
    click n4 "../modules/agent_catalog.md"
    click n5 "../modules/schemas_agent_planning.md"
    click n6 "../modules/agent_routing.md"
    click n7 "../modules/agent_model_catalog_service.md"
    click n8 "../modules/agent_service.md"
    click n9 "../modules/agent_work_service.md"
    click n10 "../modules/test_agent_model_catalog_api.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [mcp_server](../modules/mcp_server.md) |
| Inbound | [agent_catalog](../modules/agent_catalog.md) |
| Inbound | [agent_work_service](../modules/agent_work_service.md) |
| Inbound | [test_agent_model_catalog_api](../modules/test_agent_model_catalog_api.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [query_limits](../modules/query_limits.md) |
| Outbound | [schemas_agent_planning](../modules/schemas_agent_planning.md) |
| Outbound | [agent_routing](../modules/agent_routing.md) |
| Outbound | [agent_service](../modules/agent_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [AgentModelConflictError](../entities/AgentModelConflictError.md) | 52 | `AgentConflictError` | Stable model-control conflict shared by REST and MCP. |
| [_MutationResult](../entities/MutationResult.md) | 70 | — | — |
| [AgentModelCatalogService](../entities/AgentModelCatalogService.md) | 82 | — | Expose secret-free reads and replay-safe admin model mutations. |
