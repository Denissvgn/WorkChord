# list_principals

**Entry point:** `list_principals` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [authority](../modules/authority.md), [routers_identity](../modules/routers_identity.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_principals
    participant p1 as require_operator
    participant p2 as db.info.get
    participant p3 as AuthorityError
    participant p4 as (…).all
    participant p5 as db.scalars
    participant p6 as select(…).order_by(…).limit
    participant p7 as select(…).order_by
    participant p8 as select
    p0->>p1: require_operator
    p1-->>p2: db.info.get
    p1->>p3: AuthorityError
    p0-->>p4: (…).all
    p0-->>p5: db.scalars
    p0-->>p6: select(…).order_by(…).limit
    p0-->>p7: select(…).order_by
    p0-->>p8: select
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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
| list_principals | require_operator | 201 | `require_operator(db)` |
| require_operator | db.info.get | 79 | `db.info.get('authority')` |
| require_operator | AuthorityError | 81 | `AuthorityError('operator_required', 'Workspace operator permission is required.')` |
| list_principals | (…).all | 202 | `(await db.scalars(select(Principal).order_by(Principal.id).limit(limit))).all(data not statically known)` |
| list_principals | db.scalars | 202 | `db.scalars(...)` |
| list_principals | select(…).order_by(…).limit | 202 | `select(Principal).order_by(Principal.id).limit(limit)` |
| list_principals | select(…).order_by | 202 | `select(Principal).order_by(Principal.id)` |
| list_principals | select | 202 | `select(Principal)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `require_operator` | `db.info.get` | 79 |
| unresolved_call | `list_principals` | `(await db.scalars(select(Principal).order_by(Principal.id).limit(limit))).all` | 202 |
| unresolved_call | `list_principals` | `db.scalars` | 202 |
| unresolved_call | `list_principals` | `select(Principal).order_by(Principal.id).limit` | 202 |
| unresolved_call | `list_principals` | `select(Principal).order_by` | 202 |
| external_call | `list_principals` | `select` | 202 |

## Behavior

This flow starts at `list_principals` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
