# workspace_member

**Entry point:** `workspace_member` (`http`)
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
    participant p0 as workspace_member
    participant p1 as require_operator
    participant p2 as require_identity_writes
    participant p3 as AuthorityError
    participant p4 as internal_authority
    participant p5 as db.get
    participant p6 as db.delete
    participant p7 as db.add
    participant p8 as WorkspaceMembership
    participant p9 as CommandAudit
    participant p10 as db.flush
    participant p11 as db.info.get (backend/app/authority.py:require_operator)
    participant p12 as get_settings
    participant p13 as db.info.get (backend/app/authority.py:internal_authority)
    participant p14 as MaintenanceModeError
    participant p15 as Settings
    p0->>p1: require_operator
    p0->>p2: require_identity_writes
    p0->>p3: AuthorityError
    p0->>p3: AuthorityError
    p0->>p4: internal_authority
    p0-->>p5: db.get(Principal, principal_id)
    p0->>p3: AuthorityError
    p0-->>p5: db.get(WorkspaceMembership, principal_id)
    p0-->>p6: db.delete(existing)
    p0-->>p7: db.add(WorkspaceMembership(...))
    p0->>p8: WorkspaceMembership
    p0-->>p7: db.add(CommandAudit(...))
    p0->>p9: CommandAudit
    p0-->>p10: db.flush
    p1-->>p11: db.info.get (backend/app/authority.py:require_operator)('authority')
    p2->>p12: get_settings
    p4-->>p13: db.info.get (backend/app/authority.py:internal_authority)('authority_internal', False)
    p1->>p3: AuthorityError
    p2->>p14: MaintenanceModeError
    p2->>p12: get_settings
    p12->>p15: Settings
```

> Call sequence diagram shows 21 of 21 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 0 of 0 (0 omitted); unresolved 8 of 8 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 14; effect analysis evaluated: 6, partial: 0, unavailable: 8. Counts include steps omitted from the displayed trace.

Collector observations for 6 source steps with known totals: observed: 15, emitted: 15, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `workspace_member` | `available` | `evaluated` | `available` | `9` | `9` | `0` |
| `require_operator` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `db.info.get (backend/app/authority.py:require_operator)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `require_identity_writes` | `available` | `evaluated` | `available` | `0` | `0` | `0` |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `MaintenanceModeError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `internal_authority` | `available` | `evaluated` | `available` | `3` | `3` | `0` |

```mermaid
flowchart LR
    s1["1. workspace_member"]
    s2["2. require_operator"]
    s3["3. db.info.get (backend/app/authority.py:require_operator)"]
    s4["4. AuthorityError"]
    s5["5. require_identity_writes"]
    s6["6. get_settings"]
    s7["7. Settings"]
    s8["8. MaintenanceModeError"]
    s9["9. get_settings"]
    s10["10. AuthorityError"]
    s11["11. AuthorityError"]
    s12["12. internal_authority"]
    s1 -->|"require_operator(db)"| s2
    s2 -. "db.info.get (backend/app/authority.py:require_operator)('authority')" .-> s3
    s2 -->|"AuthorityError('operator_required', 'Workspace operator permission is required.')"| s4
    s1 -->|"require_identity_writes(data not statically known)"| s5
    s5 -->|"get_settings(data not statically known)"| s6
    s6 -->|"Settings(data not statically known)"| s7
    s5 -->|"MaintenanceModeError(operation='identity lifecycle', mode=...)"| s8
    s5 -->|"get_settings(data not statically known)"| s9
    s1 -->|"AuthorityError('invalid_workspace_role', 'Choose a workspace role.', 422)"| s10
    s1 -->|"AuthorityError(data not statically known)"| s11
    s1 -->|"internal_authority(db)"| s12
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
    click s11 "../modules/authority.md"
    click s12 "../modules/authority.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `workspace_member` | `principal_id: int`, `data: MembershipChange`, `db: Database` | `Principal`, `WorkspaceMembership` | `existing.role` | `{...}` |
| `require_operator` | `db` | - | - | - |
| `db.info.get (backend/app/authority.py:require_operator)` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `require_identity_writes` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `MaintenanceModeError` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `AuthorityError` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `internal_authority` | `db` | - | `db.info[...]`, `db.info[...]` | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| workspace_member | require_operator | 231 | `require_operator(db)` |
| require_operator | db.info.get (backend/app/authority.py:require_operator) | 79 | `db.info.get('authority')` |
| require_operator | AuthorityError | 81 | `AuthorityError('operator_required', 'Workspace operator permission is required.')` |
| workspace_member | require_identity_writes | 232 | `require_identity_writes(data not statically known)` |
| require_identity_writes | get_settings | 31 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| require_identity_writes | MaintenanceModeError | 32 | `MaintenanceModeError(operation='identity lifecycle', mode=...)` |
| require_identity_writes | get_settings | 32 | `get_settings(data not statically known)` |
| workspace_member | AuthorityError | 235 | `AuthorityError('invalid_workspace_role', 'Choose a workspace role.', 422)` |
| workspace_member | AuthorityError | 237 | `AuthorityError(data not statically known)` |
| workspace_member | internal_authority | 238 | `internal_authority(db)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `db.add` | `workspace_member` | 248 |
| mutation | `db.add` | `workspace_member` | 249 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `require_operator` | `db.info.get` | 79 |
| step_limit | `workspace_member` | `first 12 steps` | 0 |

## Behavior

This flow starts at `workspace_member` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
