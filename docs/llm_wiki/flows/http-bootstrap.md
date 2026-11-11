# bootstrap

**Entry point:** `bootstrap` (`http`)
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
    participant p0 as bootstrap
    participant p1 as require_identity_writes
    participant p2 as internal_authority
    participant p3 as db.get
    participant p4 as AuthorityError
    participant p5 as db.execute
    participant p6 as update(…).where(…).values
    participant p7 as update(…).where
    participant p8 as update
    participant p9 as WorkspaceAuthorityState.bootstrap_principal_id.is_
    participant p10 as db.add
    participant p11 as WorkspaceMembership
    participant p12 as CommandAudit
    participant p13 as secrets.token_hex
    participant p14 as get_settings
    participant p15 as db.info.get
    participant p16 as MaintenanceModeError
    participant p17 as Settings
    p0->>p1: require_identity_writes
    p0->>p2: internal_authority
    p0-->>p3: db.get(Principal, data.principal_id)
    p0->>p4: AuthorityError
    p0-->>p3: db.get(WorkspaceAuthorityState, 1)
    p0->>p4: AuthorityError
    p0-->>p5: db.execute(...)
    p0-->>p6: update(…).where(…).values(bootstrap_principal_id=principal.id)
    p0-->>p7: update(…).where(..., WorkspaceAuthorityState.bootstrap_principal_id.is_(...))
    p0-->>p8: update(WorkspaceAuthorityState)
    p0-->>p9: WorkspaceAuthorityState.bootstrap_principal_id.is_(None)
    p0->>p4: AuthorityError
    p0-->>p10: db.add(WorkspaceMembership(...))
    p0->>p11: WorkspaceMembership
    p0-->>p10: db.add(CommandAudit(...))
    p0->>p12: CommandAudit
    p0-->>p13: secrets.token_hex(16)
    p1->>p14: get_settings
    p2-->>p15: db.info.get('authority_internal', False)
    p1->>p16: MaintenanceModeError
    p1->>p14: get_settings
    p14->>p17: Settings
```

> Call sequence diagram shows 22 of 22 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 2 of 2 (0 omitted); unresolved 9 of 9 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 12; effect analysis evaluated: 5, partial: 0, unavailable: 7. Counts include steps omitted from the displayed trace.

Collector observations for 5 source steps with known totals: observed: 14, emitted: 14, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `bootstrap` | `available` | `evaluated` | `available` | `9` | `9` | `0` |
| `require_identity_writes` | `available` | `evaluated` | `available` | `0` | `0` | `0` |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `MaintenanceModeError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `internal_authority` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `db.info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `db.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `db.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |

```mermaid
flowchart LR
    s1["1. bootstrap"]
    s2["2. require_identity_writes"]
    s3["3. get_settings"]
    s4["4. Settings"]
    s5["5. MaintenanceModeError"]
    s6["6. get_settings"]
    s7["7. internal_authority"]
    s8["8. db.info.get"]
    s9["9. db.get"]
    s10["10. AuthorityError"]
    s11["11. db.get"]
    s12["12. AuthorityError"]
    s1 -->|"require_identity_writes(data not statically known)"| s2
    s2 -->|"get_settings(data not statically known)"| s3
    s3 -->|"Settings(data not statically known)"| s4
    s2 -->|"MaintenanceModeError(operation='identity lifecycle', mode=...)"| s5
    s2 -->|"get_settings(data not statically known)"| s6
    s1 -->|"internal_authority(db)"| s7
    s7 -. "db.info.get('authority_internal', False)" .-> s8
    s1 -. "db.get(Principal, data.principal_id)" .-> s9
    s1 -->|"AuthorityError('principal_not_found', #34;Sign in once to establish the owner's verified principal.#34;, 404)"| s10
    s1 -. "db.get(WorkspaceAuthorityState, 1)" .-> s11
    s1 -->|"AuthorityError('identity_migration_required', 'Apply the identity migration first.', 503)"| s12
    b0["mutation db.add"]
    s1 -. "mutation db.add" .-> b0
    b1["mutation db.add"]
    s1 -. "mutation db.add" .-> b1
    click s1 "../modules/routers_identity.md"
    click s2 "../modules/identity_service.md"
    click s3 "../modules/config.md"
    click s4 "../modules/config.md"
    click s5 "../modules/maintenance.md"
    click s6 "../modules/config.md"
    click s7 "../modules/authority.md"
    click s10 "../modules/authority.md"
    click s12 "../modules/authority.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `bootstrap` | `data: BootstrapOwner`, `db: Database`, `_operator: Annotated[None, Depends(require_admin_api_key)]` | `Principal`, `WorkspaceAuthorityState` | - | `{...}`, `{...}` |
| `require_identity_writes` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `MaintenanceModeError` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `internal_authority` | `db` | - | `db.info[...]`, `db.info[...]` | - |
| `db.info.get` | - | - | - | - |
| `db.get` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `db.get` | - | - | - | - |
| `AuthorityError` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| bootstrap | require_identity_writes | 212 | `require_identity_writes(data not statically known)` |
| require_identity_writes | get_settings | 31 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| require_identity_writes | MaintenanceModeError | 32 | `MaintenanceModeError(operation='identity lifecycle', mode=...)` |
| require_identity_writes | get_settings | 32 | `get_settings(data not statically known)` |
| bootstrap | internal_authority | 213 | `internal_authority(db)` |
| internal_authority | db.info.get | 87 | `db.info.get('authority_internal', False)` |
| bootstrap | db.get | 214 | `db.get(Principal, data.principal_id)` |
| bootstrap | AuthorityError | 216 | `AuthorityError('principal_not_found', "Sign in once to establish the owner's verified principal.", 404)` |
| bootstrap | db.get | 217 | `db.get(WorkspaceAuthorityState, 1)` |
| bootstrap | AuthorityError | 219 | `AuthorityError('identity_migration_required', 'Apply the identity migration first.', 503)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `db.add` | `bootstrap` | 226 |
| mutation | `db.add` | `bootstrap` | 227 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `internal_authority` | `db.info.get` | 87 |
| unresolved_call | `bootstrap` | `db.get` | 214 |
| unresolved_call | `bootstrap` | `db.get` | 217 |
| step_limit | `bootstrap` | `first 12 steps` | 0 |

## Behavior

This flow starts at `bootstrap` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

Uses the configured operator credential to assign the first verified owner through a singleton compare-and-set. Repeating bootstrap cannot replace an established owner.
