# NativeSessionService

**Location:** `backend/app/services/native_session_service.py:21`
**Kind:** Class
**Bases:** —
**Module:** [native_session_service](../modules/native_session_service.md)

## Description

Coordinates short-lived native connection requests, explicit human browser consent, and a one-use S256 proof exchange. Approval does not grant project access; the resulting session inherits the existing principal and membership policy. Revoked or expired approving sessions and disabled principals cannot issue a native session.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db)` | — | — |
| `human` | `()` | — | — |
| `connection` | *(async)* `(request_id)` | — | — |
| `start` | *(async)* `(code_challenge, ip_address)` | `@atomic_command` | — |
| `describe` | *(async)* `(request_id)` | — | — |
| `approve` | *(async)* `(request_id, verification_code)` | `@atomic_command` | — |
| `deny` | *(async)* `(request_id)` | `@atomic_command` | End a pending connection from the browser; the device's next exchange sees it as ended. |
| `exchange` | *(async)* `(request_id, code_verifier, ip_address, user_agent)` | `@atomic_command` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["NativeSessionService (backend/app/services/native_session_service.py)"]
    n1["approve_native_connection (backend/app/routers/identity.py)"]
    n2["deny_native_connection (backend/app/routers/identity.py)"]
    n3["describe_native_connection (backend/app/routers/identity.py)"]
    n4["exchange_native_connection (backend/app/routers/identity.py)"]
    n5["start_native_connection (backend/app/routers/identity.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/native_session_service.md"
    click n1 "../modules/routers_identity.md"
    click n2 "../modules/routers_identity.md"
    click n3 "../modules/routers_identity.md"
    click n4 "../modules/routers_identity.md"
    click n5 "../modules/routers_identity.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [native_session_service](../modules/native_session_service.md) | 8 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `approve_native_connection` | call | [routers_identity](../modules/routers_identity.md) | 1 |
| `deny_native_connection` | call | [routers_identity](../modules/routers_identity.md) | 1 |
| `describe_native_connection` | call | [routers_identity](../modules/routers_identity.md) | 1 |
| `exchange_native_connection` | call | [routers_identity](../modules/routers_identity.md) | 1 |
| `start_native_connection` | call | [routers_identity](../modules/routers_identity.md) | 1 |
