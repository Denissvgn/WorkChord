# MaintenanceModeError

**Location:** `backend/app/maintenance.py:25`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [maintenance](../modules/maintenance.md)

## Description

A write or non-allowlisted validation read was fenced.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(*, operation: str, mode: str)` | — | — |
| `detail` | `() -> dict[str, Any]` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MaintenanceModeError (backend/app/maintenance.py)"]
    n1["RuntimeError"]
    n2["maintenance_mode_error (backend/app/main.py)"]
    n3["enforce_mcp_access (backend/app/maintenance.py)"]
    n4["require_background_writes_enabled (backend/app/maintenance.py)"]
    n5["RuntimeBoundaryMiddleware.__call__ (backend/app/maintenance.py)"]
    n6["backend/app/mcp_server.py"]
    n7["require_identity_writes (backend/app/services/identity_service.py)"]
    n8["get_or_create_session (backend/app/services/session_service.py)"]
    n9["backend/tests/test_runtime_boundaries.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/maintenance.md"
    click n2 "../modules/app_main.md"
    click n3 "../modules/maintenance.md"
    click n4 "../modules/maintenance.md"
    click n5 "../modules/maintenance.md"
    click n6 "../modules/mcp_server.md"
    click n7 "../modules/identity_service.md"
    click n8 "../modules/session_service.md"
    click n9 "../modules/test_runtime_boundaries.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [maintenance](../modules/maintenance.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `maintenance_mode_error` | type_reference | [app_main](../modules/app_main.md) | — |
| `enforce_mcp_access` | call | [maintenance](../modules/maintenance.md) | 1 |
| `require_background_writes_enabled` | call | [maintenance](../modules/maintenance.md) | 1 |
| `RuntimeBoundaryMiddleware.__call__` | call | [maintenance](../modules/maintenance.md) | 1 |
| `mcp_server` | import | [mcp_server](../modules/mcp_server.md) | — |
| `require_identity_writes` | call | [identity_service](../modules/identity_service.md) | 1 |
| `get_or_create_session` | call | [session_service](../modules/session_service.md) | 1 |
| `test_runtime_boundaries` | import | [test_runtime_boundaries](../modules/test_runtime_boundaries.md) | — |
