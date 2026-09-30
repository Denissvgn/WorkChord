# WebIntakeRateLimiter

**Location:** `backend/app/services/web_intake_service.py:43`
**Kind:** Class
**Bases:** —
**Module:** [web_intake_service](../modules/web_intake_service.md)

## Description

In-process fixed-window rate limiter keyed by client IP.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(window_seconds: int = 60, *, clock: Callable[[], float] = time.monotonic, max_entries: int = 10000)` | — | — |
| `_evict_expired` | `(now: float) -> None` | — | Remove expired client windows without relying on wall-clock sleeps. |
| `_ensure_capacity` | `(client_ip: str) -> None` | — | Cap active-cardinality memory while retaining the current client. |
| `check` | `(client_ip: str, limit: int) -> Optional[int]` | — | Return retry-after seconds when limited, otherwise allow the request. |
| `reset` | `() -> None` | — | Clear limiter state, primarily for tests. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WebIntakeRateLimiter (backend/app/services/web_intake_service.py)"]
    n1["WebIntakeService.__init__ (backend/app/services/web_intake_service.py)"]
    n1 --> n0
    click n0 "../modules/web_intake_service.md"
    click n1 "../modules/web_intake_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [web_intake_service](../modules/web_intake_service.md) | 5 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `WebIntakeService.__init__` | type_reference | [web_intake_service](../modules/web_intake_service.md) | — |
