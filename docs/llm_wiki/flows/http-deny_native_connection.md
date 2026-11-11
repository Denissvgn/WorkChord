# deny_native_connection

**Entry point:** `deny_native_connection` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [native_session_service](../modules/native_session_service.md), [routers_identity](../modules/routers_identity.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as deny_native_connection
    participant p1 as NativeSessionService(…).deny
    participant p2 as NativeSessionService
    p0-->>p1: NativeSessionService(…).deny(request_id)
    p0->>p2: NativeSessionService
```

> Call sequence diagram shows 2 of 2 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 0 of 0 (0 omitted); unresolved 1 of 1 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 2; effect analysis evaluated: 1, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 1 source steps with known totals: observed: 5, emitted: 5, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `deny_native_connection` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `NativeSessionService(…).deny` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `NativeSessionService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |

```mermaid
flowchart LR
    s1["1. deny_native_connection"]
    s2["2. NativeSessionService(…).deny"]
    s3["3. NativeSessionService"]
    s1 -. "NativeSessionService(…).deny(request_id)" .-> s2
    s1 -->|"NativeSessionService(db)"| s3
    click s1 "../modules/routers_identity.md"
    click s3 "../modules/native_session_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `deny_native_connection` | `request_id: str`, `response: Response`, `db: Database` | - | `response.headers[...]` | `...` |
| `NativeSessionService(…).deny` | - | - | - | - |
| `NativeSessionService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| deny_native_connection | NativeSessionService(…).deny | 112 | `NativeSessionService(db).deny(request_id)` |
| deny_native_connection | NativeSessionService | 112 | `NativeSessionService(db)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `deny_native_connection` | `NativeSessionService(db).deny` | 112 |

## Behavior

This flow starts at `deny_native_connection` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
