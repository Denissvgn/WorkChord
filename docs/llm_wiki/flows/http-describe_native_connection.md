# describe_native_connection

**Entry point:** `describe_native_connection` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [native_session_service](../modules/native_session_service.md), [routers_identity](../modules/routers_identity.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as describe_native_connection
    participant p1 as NativeSessionService(…).describe
    participant p2 as NativeSessionService
    p0-->>p1: NativeSessionService(…).describe
    p0->>p2: NativeSessionService
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. describe_native_connection"]
    s2["2. NativeSessionService(…).describe"]
    s3["3. NativeSessionService"]
    s1 -. "NativeSessionService(…).describe(request_id)" .-> s2
    s1 -->|"NativeSessionService(db)"| s3
    click s1 "../modules/routers_identity.md"
    click s3 "../modules/native_session_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `describe_native_connection` | `request_id: str`, `response: Response`, `db: Database` | - | `response.headers[...]` | `...` |
| `NativeSessionService(…).describe` | - | - | - | - |
| `NativeSessionService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| describe_native_connection | NativeSessionService(…).describe | 94 | `NativeSessionService(db).describe(request_id)` |
| describe_native_connection | NativeSessionService | 94 | `NativeSessionService(db)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `describe_native_connection` | `NativeSessionService(db).describe` | 94 |

## Behavior

Requires a human session and returns only the display code, expiry, and approval state for a live connection. It does not return the challenge, approving session identity, or token.
