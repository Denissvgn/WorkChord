# task_migration_diagnostics

**Entry point:** `task_migration_diagnostics` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [authority](../modules/authority.md), [routers_task_domain](../modules/routers_task_domain.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as task_migration_diagnostics
    participant p1 as require_operator
    participant p2 as db.info.get
    participant p3 as AuthorityError
    participant p4 as (…).mappings().all
    participant p5 as (…).mappings
    participant p6 as db.execute
    participant p7 as select(…).where(…).order_by(…).limit
    participant p8 as select(…).where(…).order_by
    participant p9 as select(…).where
    participant p10 as select
    participant p11 as dict
    participant p12 as len
    p0->>p1: require_operator
    p1-->>p2: db.info.get
    p1->>p3: AuthorityError
    p0-->>p4: (…).mappings().all
    p0-->>p5: (…).mappings
    p0-->>p6: db.execute
    p0-->>p7: select(…).where(…).order_by(…).limit
    p0-->>p8: select(…).where(…).order_by
    p0-->>p9: select(…).where
    p0-->>p10: select
    p0-->>p11: dict
    p0-->>p12: len
    p0-->>p12: len
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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
| task_migration_diagnostics | require_operator | 91 | `require_operator(db)` |
| require_operator | db.info.get | 79 | `db.info.get('authority')` |
| require_operator | AuthorityError | 81 | `AuthorityError('operator_required', 'Workspace operator permission is required.')` |
| task_migration_diagnostics | (…).mappings().all | 92 | `(await db.execute(select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by(Task.id).limit(limit + 1))).mappings().all(data not statically known)` |
| task_migration_diagnostics | (…).mappings | 92 | `(await db.execute(select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by(Task.id).limit(limit + 1))).mappings(data not statically known)` |
| task_migration_diagnostics | db.execute | 92 | `db.execute(...)` |
| task_migration_diagnostics | select(…).where(…).order_by(…).limit | 92 | `select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by(Task.id).limit(...)` |
| task_migration_diagnostics | select(…).where(…).order_by | 92 | `select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by(Task.id)` |
| task_migration_diagnostics | select(…).where | 92 | `select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(...)` |
| task_migration_diagnostics | select | 92 | `select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes)` |
| task_migration_diagnostics | dict | 94 | `dict(row)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `require_operator` | `db.info.get` | 79 |
| unresolved_call | `task_migration_diagnostics` | `(await db.execute(select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by(Task.id).limit(limit + 1))).mappings().all` | 92 |
| unresolved_call | `task_migration_diagnostics` | `(await db.execute(select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by(Task.id).limit(limit + 1))).mappings` | 92 |
| unresolved_call | `task_migration_diagnostics` | `db.execute` | 92 |
| unresolved_call | `task_migration_diagnostics` | `select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by(Task.id).limit` | 92 |
| unresolved_call | `task_migration_diagnostics` | `select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by` | 92 |
| unresolved_call | `task_migration_diagnostics` | `select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate, Task.domain_backfill_version, Task.domain_migration_notes).where` | 92 |
| external_call | `task_migration_diagnostics` | `select` | 92 |
| step_limit | `task_migration_diagnostics` | `first 12 steps` | 0 |

## Behavior

This flow starts at `task_migration_diagnostics` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
