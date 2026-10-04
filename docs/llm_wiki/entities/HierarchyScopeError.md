# HierarchyScopeError

**Location:** `backend/app/commands.py:36`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [commands](../modules/commands.md)

## Description

_Auto-generated from `HierarchyScopeError` in `backend/app/commands.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `detail` | `()` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["HierarchyScopeError (backend/app/commands.py)"]
    n1["RuntimeError"]
    n2["hierarchy_scope_error (backend/app/main.py)"]
    n3["backend/app/mcp_server.py"]
    n4["aggregate_metrics (backend/app/services/work_metrics.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/commands.md"
    click n2 "../modules/app_main.md"
    click n3 "../modules/mcp_server.md"
    click n4 "../modules/services_work_metrics.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [commands](../modules/commands.md) | 1 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `hierarchy_scope_error` | type_reference | [app_main](../modules/app_main.md) | — |
| `mcp_server` | import | [mcp_server](../modules/mcp_server.md) | — |
| `aggregate_metrics` | call | [services_work_metrics](../modules/services_work_metrics.md) | 1 |
