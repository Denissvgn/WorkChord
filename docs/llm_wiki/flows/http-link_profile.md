# link_profile

**Entry point:** `link_profile` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [authority](../modules/authority.md), [config](../modules/config.md), [identity_service](../modules/identity_service.md), [maintenance](../modules/maintenance.md), and 2 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [identity_service](../modules/identity_service.md)
- [maintenance](../modules/maintenance.md)
- [models_identity](../modules/models_identity.md)
- [routers_identity](../modules/routers_identity.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as link_profile
    participant p1 as require_operator
    participant p2 as require_identity_writes
    participant p3 as internal_authority
    participant p4 as db.get
    participant p5 as AuthorityError
    participant p6 as db.scalar
    participant p7 as select(…).where
    participant p8 as select
    participant p9 as db.add
    participant p10 as PrincipalProfileLink
    participant p11 as CommandAudit
    participant p12 as db.flush
    participant p13 as db.info.get (backend/app/authority.py:require_operator)
    participant p14 as get_settings
    participant p15 as db.info.get (backend/app/authority.py:internal_authority)
    participant p16 as MaintenanceModeError
    participant p17 as Settings
    p0->>p1: require_operator
    p0->>p2: require_identity_writes
    p0->>p3: internal_authority
    p0-->>p4: db.get(Principal, principal_id)
    p0-->>p4: db.get(TeamMemberProfile, data.profile_id)
    p0->>p5: AuthorityError
    p0-->>p6: db.scalar(...)
    p0-->>p7: select(…).where(...)
    p0-->>p8: select(PrincipalProfileLink)
    p0->>p5: AuthorityError
    p0-->>p4: db.get(PrincipalProfileLink, principal_id)
    p0-->>p9: db.add(PrincipalProfileLink(...))
    p0->>p10: PrincipalProfileLink
    p0-->>p9: db.add(CommandAudit(...))
    p0->>p11: CommandAudit
    p0-->>p12: db.flush
    p1-->>p13: db.info.get (backend/app/authority.py:require_operator)('authority')
    p2->>p14: get_settings
    p3-->>p15: db.info.get (backend/app/authority.py:internal_authority)('authority_internal', False)
    p1->>p5: AuthorityError
    p2->>p16: MaintenanceModeError
    p2->>p14: get_settings
    p14->>p17: Settings
```

> Call sequence diagram shows 23 of 23 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 1 (0 omitted); unresolved 10 of 10 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 13; effect analysis evaluated: 6, partial: 0, unavailable: 7. Counts include steps omitted from the displayed trace.

Collector observations for 6 source steps with known totals: observed: 17, emitted: 17, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `link_profile` | `available` | `evaluated` | `available` | `11` | `11` | `0` |
| `require_operator` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `db.info.get (backend/app/authority.py:require_operator)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `require_identity_writes` | `available` | `evaluated` | `available` | `0` | `0` | `0` |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `MaintenanceModeError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `internal_authority` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `db.info.get (backend/app/authority.py:internal_authority)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `db.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. link_profile"]
    s2["2. require_operator"]
    s3["3. db.info.get (backend/app/authority.py:require_operator)"]
    s4["4. AuthorityError"]
    s5["5. require_identity_writes"]
    s6["6. get_settings"]
    s7["7. Settings"]
    s8["8. MaintenanceModeError"]
    s9["9. get_settings"]
    s10["10. internal_authority"]
    s11["11. db.info.get (backend/app/authority.py:internal_authority)"]
    s12["12. db.get"]
    s1 -->|"require_operator(db)"| s2
    s2 -. "db.info.get (backend/app/authority.py:require_operator)('authority')" .-> s3
    s2 -->|"AuthorityError('operator_required', 'Workspace operator permission is required.')"| s4
    s1 -->|"require_identity_writes(data not statically known)"| s5
    s5 -->|"get_settings(data not statically known)"| s6
    s6 -->|"Settings(data not statically known)"| s7
    s5 -->|"MaintenanceModeError(operation='identity lifecycle', mode=...)"| s8
    s5 -->|"get_settings(data not statically known)"| s9
    s1 -->|"internal_authority(db)"| s10
    s10 -. "db.info.get (backend/app/authority.py:internal_authority)('authority_internal', False)" .-> s11
    s1 -. "db.get(Principal, principal_id)" .-> s12
    b0["mutation db.add"]
    s1 -. "mutation db.add" .-> b0
    b1["mutation db.add"]
    s1 -. "mutation db.add" .-> b1
    click s1 "../modules/routers_identity.md"
    click s2 "../modules/authority.md"
    click s4 "../modules/authority.md"
    click s5 "../modules/identity_service.md"
    click s6 "../modules/config.md"
    click s7 "../modules/config.md"
    click s8 "../modules/maintenance.md"
    click s9 "../modules/config.md"
    click s10 "../modules/authority.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `link_profile` | `principal_id: int`, `data: ProfileLinkRequest`, `db: Database` | `Principal`, `PrincipalProfileLink`, `PrincipalProfileLink` | `link.profile_id`, `link.linked_by_principal_id` | `{...}` |
| `require_operator` | `db` | - | - | - |
| `db.info.get (backend/app/authority.py:require_operator)` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `require_identity_writes` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `MaintenanceModeError` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `internal_authority` | `db` | - | `db.info[...]`, `db.info[...]` | - |
| `db.info.get (backend/app/authority.py:internal_authority)` | - | - | - | - |
| `db.get` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| link_profile | require_operator | 260 | `require_operator(db)` |
| require_operator | db.info.get (backend/app/authority.py:require_operator) | 79 | `db.info.get('authority')` |
| require_operator | AuthorityError | 81 | `AuthorityError('operator_required', 'Workspace operator permission is required.')` |
| link_profile | require_identity_writes | 261 | `require_identity_writes(data not statically known)` |
| require_identity_writes | get_settings | 31 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| require_identity_writes | MaintenanceModeError | 32 | `MaintenanceModeError(operation='identity lifecycle', mode=...)` |
| require_identity_writes | get_settings | 32 | `get_settings(data not statically known)` |
| link_profile | internal_authority | 263 | `internal_authority(db)` |
| internal_authority | db.info.get (backend/app/authority.py:internal_authority) | 87 | `db.info.get('authority_internal', False)` |
| link_profile | db.get | 264 | `db.get(Principal, principal_id)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `db.add` | `link_profile` | 275 |
| mutation | `db.add` | `link_profile` | 277 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `require_operator` | `db.info.get` | 79 |
| unresolved_call | `internal_authority` | `db.info.get` | 87 |
| unresolved_call | `link_profile` | `db.get` | 264 |
| step_limit | `link_profile` | `first 12 steps` | 0 |

## Behavior

This flow starts at `link_profile` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
