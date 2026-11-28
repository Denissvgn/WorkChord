# AgentModelConflictError

**Location:** `backend/app/services/agent_model_catalog_service.py:58`
**Kind:** Class
**Bases:** `AgentConflictError`
**Module:** [agent_model_catalog_service](../modules/agent_model_catalog_service.md)

## Description

Stable model-control conflict shared by REST and MCP.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(code: str, message: str, **context: Any)` | — | — |
| `detail` | `() -> dict[str, Any]` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentModelConflictError (backend/app/services/agent_model_catalog_service.py)"]
    n1["AgentConflictError (backend/app/services/agent_service.py)"]
    n2["backend/app/mcp_server.py"]
    n3["backend/app/routers/agent_catalog.py"]
    n4["AgentModelCatalogService._execute (backend/app/services/agent_model_catalog_service.py)"]
    n5["AgentModelCatalogService._live_assignments (backend/app/services/agent_model_catalog_service.py)"]
    n6["AgentModelCatalogService._locked_binding (backend/app/services/agent_model_catalog_service.py)"]
    n7["AgentModelCatalogService._raise_revision_conflict (backend/app/services/agent_model_catalog_service.py)"]
    n8["AgentModelCatalogService._replay (backend/app/services/agent_model_catalog_service.py)"]
    n9["AgentModelCatalogService._require_default_slot (backend/app/services/agent_model_catalog_service.py)"]
    n10["AgentModelCatalogService._require_reconciliation (backend/app/services/agent_model_catalog_service.py)"]
    n11["reconcile_execution (backend/app/services/execution_reconciliation.py)"]
    n12["reconcile_window (backend/app/services/planning_window_reconciliation.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    click n0 "../modules/agent_model_catalog_service.md"
    click n1 "../modules/agent_service.md"
    click n2 "../modules/mcp_server.md"
    click n3 "../modules/agent_catalog.md"
    click n4 "../modules/agent_model_catalog_service.md"
    click n5 "../modules/agent_model_catalog_service.md"
    click n6 "../modules/agent_model_catalog_service.md"
    click n7 "../modules/agent_model_catalog_service.md"
    click n8 "../modules/agent_model_catalog_service.md"
    click n9 "../modules/agent_model_catalog_service.md"
    click n10 "../modules/agent_model_catalog_service.md"
    click n11 "../modules/execution_reconciliation.md"
    click n12 "../modules/planning_window_reconciliation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `AgentConflictError` | [agent_service](../modules/agent_service.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_server` | import | [mcp_server](../modules/mcp_server.md) | — |
| `agent_catalog` | import | [agent_catalog](../modules/agent_catalog.md) | — |
| `AgentModelCatalogService._execute` | call | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | 1 |
| `AgentModelCatalogService._execute` | type_reference | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | — |
| `AgentModelCatalogService._live_assignments` | call | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | 1 |
| `AgentModelCatalogService._locked_binding` | call | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | 2 |
| `AgentModelCatalogService._raise_revision_conflict` | call | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | 1 |
| `AgentModelCatalogService._replay` | call | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | 2 |
| `AgentModelCatalogService._require_default_slot` | call | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | 1 |
| `AgentModelCatalogService._require_reconciliation` | call | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | 1 |
| `reconcile_execution` | call | [execution_reconciliation](../modules/execution_reconciliation.md) | 2 |
| `reconcile_window` | call | [planning_window_reconciliation](../modules/planning_window_reconciliation.md) | 2 |

> References: showing 12 of 24 logical references; 12 omitted by the 12-row generated summary limit.
