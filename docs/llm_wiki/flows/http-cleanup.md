# cleanup

**Entry point:** `cleanup` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [identity_service](../modules/identity_service.md), [routers_identity](../modules/routers_identity.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as cleanup
    participant p1 as IdentityService(…).cleanup_sessions
    participant p2 as IdentityService
    p0-->>p1: IdentityService(…).cleanup_sessions
    p0->>p2: IdentityService
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. cleanup"]
    s2["2. IdentityService(…).cleanup_sessions"]
    s3["3. IdentityService"]
    s1 -. "IdentityService(…).cleanup_sessions(limit=limit)" .-> s2
    s1 -->|"IdentityService(db)"| s3
    click s1 "../modules/routers_identity.md"
    click s3 "../modules/identity_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `cleanup` | `db: Database`, `limit: int` | - | - | `...` |
| `IdentityService(…).cleanup_sessions` | - | - | - | - |
| `IdentityService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| cleanup | IdentityService(…).cleanup_sessions | 340 | `IdentityService(db).cleanup_sessions(limit=limit)` |
| cleanup | IdentityService | 340 | `IdentityService(db)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `cleanup` | `IdentityService(db).cleanup_sessions` | 340 |

## Behavior

This flow starts at `cleanup` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
