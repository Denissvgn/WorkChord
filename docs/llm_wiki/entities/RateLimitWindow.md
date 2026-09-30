# _RateLimitWindow

**Location:** `backend/app/services/web_intake_service.py:38`
**Kind:** Class
**Bases:** —
**Module:** [web_intake_service](../modules/web_intake_service.md)

**Decorators:** `@dataclass`

## Description

_Auto-generated from `_RateLimitWindow` in `backend/app/services/web_intake_service.py`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `window_started_at` | `float` | *required* | — |
| `count` | `int` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["_RateLimitWindow (backend/app/services/web_intake_service.py)"]
    n1["WebIntakeRateLimiter.check (backend/app/services/web_intake_service.py)"]
    n1 --> n0
    click n0 "../modules/web_intake_service.md"
    click n1 "../modules/web_intake_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [web_intake_service](../modules/web_intake_service.md) | 0 | `count`, `window_started_at` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `WebIntakeRateLimiter.check` | call | [web_intake_service](../modules/web_intake_service.md) | 1 |
