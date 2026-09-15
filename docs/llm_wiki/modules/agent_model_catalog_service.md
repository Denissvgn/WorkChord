# agent_model_catalog_service Module

**Path:** `backend/app/services/agent_model_catalog_service.py`

## Description

Operator-owned model catalog, binding administration, and audit receipts.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.commands` | `commit_or_flush` |
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
    n0["backend/app/commands.py"]
    n1["backend/app/mcp_agent_tools.py"]
    n2["backend/app/mcp_server.py"]
    n3["backend/app/models/agent.py"]
    n4["backend/app/query_limits.py"]
    n5["backend/app/routers/agent_catalog.py"]
    n6["backend/app/schemas/agent_planning.py"]
    n7["backend/app/schemas/agent_routing.py"]
    n8["backend/app/services/agent_model_catalog_service.py"]
    n9["backend/app/services/agent_service.py"]
    n10["backend/app/services/agent_work_service.py"]
    n11["backend/tests/test_agent_model_catalog_api.py"]
    n1 --> n0
    n1 --> n3
    n1 --> n6
    n1 --> n7
    n1 --> n8
    n1 --> n9
    n1 --> n10
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n8
    n2 --> n9
    n5 --> n3
    n5 --> n6
    n5 --> n7
    n5 --> n8
    n5 --> n9
    n8 --> n0
    n8 --> n3
    n8 --> n4
    n8 --> n6
    n8 --> n7
    n8 --> n9
    n9 --> n0
    n9 --> n3
    n9 --> n4
    n10 --> n0
    n10 --> n3
    n10 --> n4
    n10 --> n6
    n10 --> n8
    n10 --> n9
    n11 --> n1
    n11 --> n2
    n11 --> n3
    n11 --> n6
    n11 --> n7
    n11 --> n8
    n11 --> n9
    n11 --> n10
    click n0 "../modules/commands.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/mcp_server.md"
    click n3 "../modules/models_agent.md"
    click n4 "../modules/query_limits.md"
    click n5 "../modules/agent_catalog.md"
    click n6 "../modules/schemas_agent_planning.md"
    click n7 "../modules/agent_routing.md"
    click n8 "../modules/agent_model_catalog_service.md"
    click n9 "../modules/agent_service.md"
    click n10 "../modules/agent_work_service.md"
    click n11 "../modules/test_agent_model_catalog_api.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [mcp_server](../modules/mcp_server.md) |
| Inbound | [agent_catalog](../modules/agent_catalog.md) |
| Inbound | [agent_work_service](../modules/agent_work_service.md) |
| Inbound | [test_agent_model_catalog_api](../modules/test_agent_model_catalog_api.md) |
| Outbound | [commands](../modules/commands.md) |
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
| [AgentModelConflictError](../entities/AgentModelConflictError.md) | 54 | `AgentConflictError` | Stable model-control conflict shared by REST and MCP. |
| [_MutationResult](../entities/MutationResult.md) | 72 | — | — |
| [AgentModelCatalogService](../entities/AgentModelCatalogService.md) | 84 | — | Expose secret-free reads and replay-safe admin model mutations. |
