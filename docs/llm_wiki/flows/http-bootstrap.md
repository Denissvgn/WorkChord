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

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as bootstrap
    participant p1 as require_identity_writes
    participant p2 as get_settings
    participant p3 as Settings
    participant p4 as MaintenanceModeError
    participant p5 as internal_authority
    participant p6 as db.info.get
    participant p7 as db.get
    participant p8 as AuthorityError
    participant p9 as db.execute
    participant p10 as update(…).where(…).values
    participant p11 as update(…).where
    participant p12 as update
    participant p13 as WorkspaceAuthorityState.bootstrap_principal_id.is_
    participant p14 as db.add
    participant p15 as WorkspaceMembership
    participant p16 as CommandAudit
    participant p17 as secrets.token_hex
    p0->>p1: require_identity_writes
    p1->>p2: get_settings
    p2->>p3: Settings
    p1->>p4: MaintenanceModeError
    p1->>p2: get_settings
    p0->>p5: internal_authority
    p5-->>p6: db.info.get
    p0-->>p7: db.get
    p0->>p8: AuthorityError
    p0-->>p7: db.get
    p0->>p8: AuthorityError
    p0-->>p9: db.execute
    p0-->>p10: update(…).where(…).values
    p0-->>p11: update(…).where
    p0-->>p12: update
    p0-->>p13: WorkspaceAuthorityState.bootstrap_principal_id.is_
    p0->>p8: AuthorityError
    p0-->>p14: db.add
    p0->>p15: WorkspaceMembership
    p0-->>p14: db.add
    p0->>p16: CommandAudit
    p0-->>p17: secrets.token_hex
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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
| bootstrap | require_identity_writes | 178 | `require_identity_writes(data not statically known)` |
| require_identity_writes | get_settings | 31 | `get_settings(data not statically known)` |
| get_settings | Settings | 480 | `Settings(data not statically known)` |
| require_identity_writes | MaintenanceModeError | 32 | `MaintenanceModeError(operation='identity lifecycle', mode=...)` |
| require_identity_writes | get_settings | 32 | `get_settings(data not statically known)` |
| bootstrap | internal_authority | 179 | `internal_authority(db)` |
| internal_authority | db.info.get | 87 | `db.info.get('authority_internal', False)` |
| bootstrap | db.get | 180 | `db.get(Principal, data.principal_id)` |
| bootstrap | AuthorityError | 182 | `AuthorityError('principal_not_found', "Sign in once to establish the owner's verified principal.", 404)` |
| bootstrap | db.get | 183 | `db.get(WorkspaceAuthorityState, 1)` |
| bootstrap | AuthorityError | 185 | `AuthorityError('identity_migration_required', 'Apply the identity migration first.', 503)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `db.add` | `bootstrap` | 192 |
| mutation | `db.add` | `bootstrap` | 193 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `internal_authority` | `db.info.get` | 87 |
| unresolved_call | `bootstrap` | `db.get` | 180 |
| unresolved_call | `bootstrap` | `db.get` | 183 |
| step_limit | `bootstrap` | `first 12 steps` | 0 |

## Behavior

This flow starts at `bootstrap` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

Uses the configured operator credential to assign the first verified owner through a singleton compare-and-set. Repeating bootstrap cannot replace an established owner.
