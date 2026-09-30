# maintenance Module

**Path:** `backend/app/maintenance.py`

## Description

Fail-closed maintenance/validation authority shared by REST, MCP, and workers.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.config` | `get_settings` |
| `app.runtime_telemetry` | `activity`, `correlation_id_context`, `metrics` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `re` | `re` |
| `socket` | `socket` |
| `starlette.responses` | `JSONResponse` |
| `starlette.types` | `ASGIApp`, `Message`, `Receive`, `Scope`, `Send` |
| `time` | `monotonic` |
| `typing` | `Any` |
| `uuid` | `uuid4` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/config.py"]
    n1["backend/app/main.py"]
    n2["backend/app/maintenance.py"]
    n3["backend/app/mcp_server.py"]
    n4["backend/app/observability.py"]
    n5["backend/app/runtime_telemetry.py"]
    n6["backend/app/services/identity_service.py"]
    n7["backend/app/services/outbound_webhook_service.py"]
    n8["backend/app/services/session_service.py"]
    n9["backend/app/services/upgrade_service.py"]
    n10["backend/tests/test_runtime_boundaries.py"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n2 --> n0
    n2 --> n5
    n3 --> n0
    n3 --> n2
    n3 --> n6
    n4 --> n0
    n4 --> n2
    n4 --> n5
    n4 --> n9
    n6 --> n0
    n6 --> n2
    n7 --> n2
    n7 --> n5
    n8 --> n0
    n8 --> n2
    n8 --> n5
    n8 --> n6
    n9 --> n0
    n9 --> n2
    n9 --> n6
    n10 --> n0
    n10 --> n1
    n10 --> n2
    n10 --> n8
    click n0 "../modules/config.md"
    click n1 "../modules/app_main.md"
    click n2 "../modules/maintenance.md"
    click n3 "../modules/mcp_server.md"
    click n4 "../modules/observability.md"
    click n5 "../modules/runtime_telemetry.md"
    click n6 "../modules/identity_service.md"
    click n7 "../modules/outbound_webhook_service.md"
    click n8 "../modules/session_service.md"
    click n9 "../modules/upgrade_service.md"
    click n10 "../modules/test_runtime_boundaries.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [app_main](../modules/app_main.md) |
| Inbound | [mcp_server](../modules/mcp_server.md) |
| Inbound | [observability](../modules/observability.md) |
| Inbound | [identity_service](../modules/identity_service.md) |
| Inbound | [outbound_webhook_service](../modules/outbound_webhook_service.md) |
| Inbound | [session_service](../modules/session_service.md) |
| Inbound | [upgrade_service](../modules/upgrade_service.md) |
| Inbound | [test_runtime_boundaries](../modules/test_runtime_boundaries.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [runtime_telemetry](../modules/runtime_telemetry.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [MaintenanceModeError](../entities/MaintenanceModeError.md) | 25 | `RuntimeError` | A write or non-allowlisted validation read was fenced. |
| [RuntimeBoundaryMiddleware](../entities/RuntimeBoundaryMiddleware.md) | 134 | — | Enforce REST fencing and record bounded request/drain telemetry. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `maintenance_configuration_fingerprint` | `() -> str` | — | Identify the complete restart-bound fence configuration. |
| `maintenance_state` | `() -> dict[str, Any]` | — | — |
| `_path_allowed` | `(path: str, allowlist: list[str]) -> bool` | — | — |
| `_is_mcp_path` | `(path: str) -> bool` | — | — |
| `scope_requirement_is_mutating` | `(required_scope: Any) -> bool` | — | Classify MCP mutations from their enforced authorization contract. |
| `enforce_mcp_access` | `(required_scope: Any) -> None` | — | Fence every scope-classified MCP mutation before opening a transaction. |
| `require_background_writes_enabled` | `(operation: str) -> None` | — | Fence worker, seed, and repair writes under the same deployment mode. |
| `_header` | `(scope: Scope, name: str) -> str \| None` | — | — |
