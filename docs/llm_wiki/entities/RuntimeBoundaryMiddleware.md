# RuntimeBoundaryMiddleware

**Location:** `backend/app/maintenance.py:134`
**Kind:** Class
**Bases:** —
**Module:** [maintenance](../modules/maintenance.md)

## Description

Enforce REST fencing and record bounded request/drain telemetry.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(app: ASGIApp)` | — | — |
| `__call__` | *(async)* `(scope: Scope, receive: Receive, send: Send) -> None` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RuntimeBoundaryMiddleware (backend/app/maintenance.py)"]
    n1["backend/app/main.py"]
    n2["backend/tests/test_runtime_boundaries.py"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/maintenance.md"
    click n1 "../modules/app_main.md"
    click n2 "../modules/test_runtime_boundaries.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [maintenance](../modules/maintenance.md) | 2 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `main` | import | [app_main](../modules/app_main.md) | — |
| `test_runtime_boundaries` | import | [test_runtime_boundaries](../modules/test_runtime_boundaries.md) | — |
