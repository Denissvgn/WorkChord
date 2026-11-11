# cleanup

**Entry point:** `cleanup` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [identity_service](../modules/identity_service.md), [routers_identity](../modules/routers_identity.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as cleanup
    participant p1 as IdentityService(…).cleanup_sessions
    participant p2 as IdentityService
    p0-->>p1: IdentityService(…).cleanup_sessions(limit=limit)
    p0->>p2: IdentityService
```

> Call sequence diagram shows 2 of 2 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 0 of 0 (0 omitted); unresolved 1 of 1 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 2; effect analysis evaluated: 1, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 1 source steps with known totals: observed: 3, emitted: 3, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `cleanup` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `IdentityService(…).cleanup_sessions` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `IdentityService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |

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
| cleanup | IdentityService(…).cleanup_sessions | 363 | `IdentityService(db).cleanup_sessions(limit=limit)` |
| cleanup | IdentityService | 363 | `IdentityService(db)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `cleanup` | `IdentityService(db).cleanup_sessions` | 363 |

## Behavior

This flow starts at `cleanup` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
