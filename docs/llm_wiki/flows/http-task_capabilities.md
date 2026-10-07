# task_capabilities

**Entry point:** `task_capabilities` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [authority](../modules/authority.md), [config](../modules/config.md), [routers_task_domain](../modules/routers_task_domain.md), [task_domain_service](../modules/task_domain_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as task_capabilities
    participant p1 as domain_capabilities
    participant p2 as internal_authority
    participant p3 as db.info.get
    participant p4 as db.scalar
    participant p5 as select(…).where(…).limit
    participant p6 as select(…).where
    participant p7 as select
    participant p8 as get_settings
    participant p9 as Settings
    p0->>p1: domain_capabilities
    p1->>p2: internal_authority
    p2-->>p3: db.info.get
    p1-->>p4: db.scalar
    p1-->>p5: select(…).where(…).limit
    p1-->>p6: select(…).where
    p1-->>p7: select
    p1->>p8: get_settings
    p8->>p9: Settings
    p1->>p8: get_settings
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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
| task_capabilities | domain_capabilities | 72 | `domain_capabilities(db)` |
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

*No boundary effects detected.*

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
