# list_principals

**Entry point:** `list_principals` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [authority](../modules/authority.md), [routers_identity](../modules/routers_identity.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_principals
    participant p1 as require_operator
    participant p2 as (…).all
    participant p3 as db.scalars
    participant p4 as select(…).order_by(…).limit
    participant p5 as select(…).order_by
    participant p6 as select
    participant p7 as db.info.get
    participant p8 as AuthorityError
    p0->>p1: require_operator
    p0-->>p2: (…).all
    p0-->>p3: db.scalars(...)
    p0-->>p4: select(…).order_by(…).limit(limit)
    p0-->>p5: select(…).order_by(Principal.id)
    p0-->>p6: select(Principal)
    p1-->>p7: db.info.get('authority')
    p1->>p8: AuthorityError
```

> Call sequence diagram shows 8 of 8 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 1 (0 omitted); unresolved 5 of 5 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 3; effect analysis evaluated: 2, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 2 source steps with known totals: observed: 4, emitted: 4, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `list_principals` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `require_operator` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `db.info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `(…).all` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `db.scalars` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).order_by(…).limit` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).order_by` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. list_principals"]
    s2["2. require_operator"]
    s3["3. db.info.get"]
    s4["4. AuthorityError"]
    s5["5. (…).all"]
    s6["6. db.scalars"]
    s7["7. select(…).order_by(…).limit"]
    s8["8. select(…).order_by"]
    s9["9. select"]
    s1 -->|"require_operator(db)"| s2
    s2 -. "db.info.get('authority')" .-> s3
    s2 -->|"AuthorityError('operator_required', 'Workspace operator permission is required.')"| s4
    s1 -. "(…).all(data not statically known)" .-> s5
    s1 -. "db.scalars(...)" .-> s6
    s1 -. "select(…).order_by(…).limit(limit)" .-> s7
    s1 -. "select(…).order_by(Principal.id)" .-> s8
    s1 -. "select(Principal)" .-> s9
    click s1 "../modules/routers_identity.md"
    click s2 "../modules/authority.md"
    click s4 "../modules/authority.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_principals` | `db: Database`, `limit: int` | - | - | `...` |
| `require_operator` | `db` | - | - | - |
| `db.info.get` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `(…).all` | - | - | - | - |
| `db.scalars` | - | - | - | - |
| `select(…).order_by(…).limit` | - | - | - | - |
| `select(…).order_by` | - | - | - | - |
| `select` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_principals | require_operator | 235 | `require_operator(db)` |
| require_operator | db.info.get | 79 | `db.info.get('authority')` |
| require_operator | AuthorityError | 81 | `AuthorityError('operator_required', 'Workspace operator permission is required.')` |
| list_principals | (…).all | 236 | `(await db.scalars(select(Principal).order_by(Principal.id).limit(limit))).all(data not statically known)` |
| list_principals | db.scalars | 236 | `db.scalars(...)` |
| list_principals | select(…).order_by(…).limit | 236 | `select(Principal).order_by(Principal.id).limit(limit)` |
| list_principals | select(…).order_by | 236 | `select(Principal).order_by(Principal.id)` |
| list_principals | select | 236 | `select(Principal)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `require_operator` | `db.info.get` | 79 |
| unresolved_call | `list_principals` | `(await db.scalars(select(Principal).order_by(Principal.id).limit(limit))).all` | 236 |
| unresolved_call | `list_principals` | `db.scalars` | 236 |
| unresolved_call | `list_principals` | `select(Principal).order_by(Principal.id).limit` | 236 |
| unresolved_call | `list_principals` | `select(Principal).order_by` | 236 |
| external_call | `list_principals` | `select` | 236 |

## Behavior

This flow starts at `list_principals` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
