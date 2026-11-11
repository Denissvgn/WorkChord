# task_capabilities

**Entry point:** `task_capabilities` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [authority](../modules/authority.md), [config](../modules/config.md), [routers_task_domain](../modules/routers_task_domain.md), [task_domain_service](../modules/task_domain_service.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as task_capabilities
    participant p1 as domain_capabilities
    participant p2 as internal_authority
    participant p3 as db.scalar
    participant p4 as select(…).where(…).limit
    participant p5 as select(…).where
    participant p6 as select
    participant p7 as get_settings
    participant p8 as db.info.get
    participant p9 as Settings
    p0->>p1: domain_capabilities
    p1->>p2: internal_authority
    p1-->>p3: db.scalar(...)
    p1-->>p4: select(…).where(…).limit(1)
    p1-->>p5: select(…).where(...)
    p1-->>p6: select(Task.id)
    p1->>p7: get_settings
    p1->>p7: get_settings
    p2-->>p8: db.info.get('authority_internal', False)
    p7->>p9: Settings
```

> Call sequence diagram shows 10 of 10 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 1 (0 omitted); unresolved 4 of 4 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 6; effect analysis evaluated: 5, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 5 source steps with known totals: observed: 10, emitted: 10, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `task_capabilities` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `domain_capabilities` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `internal_authority` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `db.info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `db.scalar` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).where(…).limit` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).where` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |

```mermaid
flowchart LR
    s1["1. task_capabilities"]
    s2["2. domain_capabilities"]
    s3["3. internal_authority"]
    s4["4. db.info.get"]
    s5["5. db.scalar"]
    s6["6. select(…).where(…).limit"]
    s7["7. select(…).where"]
    s8["8. select"]
    s9["9. get_settings"]
    s10["10. Settings"]
    s11["11. get_settings"]
    s1 -->|"domain_capabilities(db)"| s2
    s2 -->|"internal_authority(db)"| s3
    s3 -. "db.info.get('authority_internal', False)" .-> s4
    s2 -. "db.scalar(...)" .-> s5
    s2 -. "select(…).where(…).limit(1)" .-> s6
    s2 -. "select(…).where(...)" .-> s7
    s2 -. "select(Task.id)" .-> s8
    s2 -->|"get_settings(data not statically known)"| s9
    s9 -->|"Settings(data not statically known)"| s10
    s2 -->|"get_settings(data not statically known)"| s11
    click s1 "../modules/routers_task_domain.md"
    click s2 "../modules/task_domain_service.md"
    click s3 "../modules/authority.md"
    click s9 "../modules/config.md"
    click s10 "../modules/config.md"
    click s11 "../modules/config.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `task_capabilities` | `db: DB` | - | - | `...` |
| `domain_capabilities` | `db` | - | - | `{...}`, `{...}` |
| `internal_authority` | `db` | - | `db.info[...]`, `db.info[...]` | - |
| `db.info.get` | - | - | - | - |
| `db.scalar` | - | - | - | - |
| `select(…).where(…).limit` | - | - | - | - |
| `select(…).where` | - | - | - | - |
| `select` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| task_capabilities | domain_capabilities | 127 | `domain_capabilities(db)` |
| domain_capabilities | internal_authority | 56 | `internal_authority(db)` |
| internal_authority | db.info.get | 87 | `db.info.get('authority_internal', False)` |
| domain_capabilities | db.scalar | 57 | `db.scalar(...)` |
| domain_capabilities | select(…).where(…).limit | 57 | `select(Task.id).where(Task.domain_backfill_version < 1).limit(1)` |
| domain_capabilities | select(…).where | 57 | `select(Task.id).where(...)` |
| domain_capabilities | select | 57 | `select(Task.id)` |
| domain_capabilities | get_settings | 61 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| domain_capabilities | get_settings | 62 | `get_settings(data not statically known)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `internal_authority` | `db.info.get` | 87 |
| unresolved_call | `domain_capabilities` | `db.scalar` | 57 |
| unresolved_call | `domain_capabilities` | `select(Task.id).where(Task.domain_backfill_version < 1).limit` | 57 |
| unresolved_call | `domain_capabilities` | `select(Task.id).where` | 57 |
| external_call | `domain_capabilities` | `select` | 57 |

## Behavior

This flow starts at `task_capabilities` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
