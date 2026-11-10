# task_migration_diagnostics

**Entry point:** `task_migration_diagnostics` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [authority](../modules/authority.md), [routers_task_domain](../modules/routers_task_domain.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as task_migration_diagnostics
    participant p1 as require_operator
    participant p2 as (…).mappings().all
    participant p3 as (…).mappings
    participant p4 as db.execute
    participant p5 as select(…).where(…).order_by(…).limit
    participant p6 as select(…).where(…).order_by
    participant p7 as select(…).where
    participant p8 as select
    participant p9 as dict
    participant p10 as len
    participant p11 as db.info.get
    participant p12 as AuthorityError
    p0->>p1: require_operator
    p0-->>p2: (…).mappings().all
    p0-->>p3: (…).mappings
    p0-->>p4: db.execute(...)
    p0-->>p5: select(…).where(…).order_by(…).limit(...)
    p0-->>p6: select(…).where(…).order_by(Task.id)
    p0-->>p7: select(…).where(...)
    p0-->>p8: select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes)
    p0-->>p9: dict(row)
    p0-->>p10: len(rows)
    p0-->>p10: len(rows)
    p1-->>p11: db.info.get('authority')
    p1->>p12: AuthorityError
```

> Call sequence diagram shows 13 of 13 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 4 of 4 (0 omitted); unresolved 7 of 7 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 3; effect analysis evaluated: 2, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 2 source steps with known totals: observed: 5, emitted: 5, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `task_migration_diagnostics` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `require_operator` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `db.info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `(…).mappings().all` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `(…).mappings` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `db.execute` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).where(…).order_by(…).limit` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).where(…).order_by` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).where` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `dict` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. task_migration_diagnostics"]
    s2["2. require_operator"]
    s3["3. db.info.get"]
    s4["4. AuthorityError"]
    s5["5. (…).mappings().all"]
    s6["6. (…).mappings"]
    s7["7. db.execute"]
    s8["8. select(…).where(…).order_by(…).limit"]
    s9["9. select(…).where(…).order_by"]
    s10["10. select(…).where"]
    s11["11. select"]
    s12["12. dict"]
    s1 -->|"require_operator(db)"| s2
    s2 -. "db.info.get('authority')" .-> s3
    s2 -->|"AuthorityError('operator_required', 'Workspace operator permission is required.')"| s4
    s1 -. "(…).mappings().all(data not statically known)" .-> s5
    s1 -. "(…).mappings(data not statically known)" .-> s6
    s1 -. "db.execute(...)" .-> s7
    s1 -. "select(…).where(…).order_by(…).limit(...)" .-> s8
    s1 -. "select(…).where(…).order_by(Task.id)" .-> s9
    s1 -. "select(…).where(...)" .-> s10
    s1 -. "select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes)" .-> s11
    s1 -. "dict(row)" .-> s12
    click s1 "../modules/routers_task_domain.md"
    click s2 "../modules/authority.md"
    click s4 "../modules/authority.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `task_migration_diagnostics` | `db: DB`, `after_id: int`, `limit: int` | - | - | `{...}` |
| `require_operator` | `db` | - | - | - |
| `db.info.get` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `(…).mappings().all` | - | - | - | - |
| `(…).mappings` | - | - | - | - |
| `db.execute` | - | - | - | - |
| `select(…).where(…).order_by(…).limit` | - | - | - | - |
| `select(…).where(…).order_by` | - | - | - | - |
| `select(…).where` | - | - | - | - |
| `select` | - | - | - | - |
| `dict` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| task_migration_diagnostics | require_operator | 129 | `require_operator(db)` |
| require_operator | db.info.get | 79 | `db.info.get('authority')` |
| require_operator | AuthorityError | 81 | `AuthorityError('operator_required', 'Workspace operator permission is required.')` |
| task_migration_diagnostics | (…).mappings().all | 130 | `(await db.execute(select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by(Task.id).limit(limit + 1))).mappings().all(data not statically known)` |
| task_migration_diagnostics | (…).mappings | 130 | `(await db.execute(select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by(Task.id).limit(limit + 1))).mappings(data not statically known)` |
| task_migration_diagnostics | db.execute | 130 | `db.execute(...)` |
| task_migration_diagnostics | select(…).where(…).order_by(…).limit | 130 | `select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by(Task.id).limit(...)` |
| task_migration_diagnostics | select(…).where(…).order_by | 130 | `select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by(Task.id)` |
| task_migration_diagnostics | select(…).where | 130 | `select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(...)` |
| task_migration_diagnostics | select | 130 | `select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes)` |
| task_migration_diagnostics | dict | 132 | `dict(row)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `require_operator` | `db.info.get` | 79 |
| unresolved_call | `task_migration_diagnostics` | `(await db.execute(select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by(Task.id).limit(limit + 1))).mappings().all` | 130 |
| unresolved_call | `task_migration_diagnostics` | `(await db.execute(select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by(Task.id).limit(limit + 1))).mappings` | 130 |
| unresolved_call | `task_migration_diagnostics` | `db.execute` | 130 |
| unresolved_call | `task_migration_diagnostics` | `select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by(Task.id).limit` | 130 |
| unresolved_call | `task_migration_diagnostics` | `select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by` | 130 |
| unresolved_call | `task_migration_diagnostics` | `select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where` | 130 |
| external_call | `task_migration_diagnostics` | `select` | 130 |
| step_limit | `task_migration_diagnostics` | `first 12 steps` | 0 |

## Behavior

This flow starts at `task_migration_diagnostics` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
