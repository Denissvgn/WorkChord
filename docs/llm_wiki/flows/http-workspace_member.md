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

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as workspace_member
    participant p1 as require_operator
    participant p2 as db.info.get (backend/app/authority.py:require_operator)
    participant p3 as AuthorityError
    participant p4 as require_identity_writes
    participant p5 as get_settings
    participant p6 as Settings
    participant p7 as MaintenanceModeError
    participant p8 as internal_authority
    participant p9 as db.info.get (backend/app/authority.py:internal_authority)
    participant p10 as db.get
    participant p11 as db.delete
    participant p12 as db.add
    participant p13 as WorkspaceMembership
    participant p14 as CommandAudit
    participant p15 as db.flush
    p0->>p1: require_operator
    p1-->>p2: db.info.get (backend/app/authority.py:require_operator)
    p1->>p3: AuthorityError
    p0->>p4: require_identity_writes
    p4->>p5: get_settings
    p5->>p6: Settings
    p4->>p7: MaintenanceModeError
    p4->>p5: get_settings
    p0->>p3: AuthorityError
    p0->>p3: AuthorityError
    p0->>p8: internal_authority
    p8-->>p9: db.info.get (backend/app/authority.py:internal_authority)
    p0-->>p10: db.get
    p0->>p3: AuthorityError
    p0-->>p10: db.get
    p0-->>p11: db.delete
    p0-->>p12: db.add
    p0->>p13: WorkspaceMembership
    p0-->>p12: db.add
    p0->>p14: CommandAudit
    p0-->>p15: db.flush
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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
| workspace_member | require_operator | 208 | `require_operator(db)` |
| require_operator | db.info.get (backend/app/authority.py:require_operator) | 79 | `db.info.get('authority')` |
| require_operator | AuthorityError | 81 | `AuthorityError('operator_required', 'Workspace operator permission is required.')` |
| workspace_member | require_identity_writes | 209 | `require_identity_writes(data not statically known)` |
| require_identity_writes | get_settings | 31 | `get_settings(data not statically known)` |
| get_settings | Settings | 480 | `Settings(data not statically known)` |
| require_identity_writes | MaintenanceModeError | 32 | `MaintenanceModeError(operation='identity lifecycle', mode=...)` |
| require_identity_writes | get_settings | 32 | `get_settings(data not statically known)` |
| workspace_member | AuthorityError | 212 | `AuthorityError('invalid_workspace_role', 'Choose a workspace role.', 422)` |
| workspace_member | AuthorityError | 214 | `AuthorityError(data not statically known)` |
| workspace_member | internal_authority | 215 | `internal_authority(db)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `db.add` | `workspace_member` | 225 |
| mutation | `db.add` | `workspace_member` | 226 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `require_operator` | `db.info.get` | 79 |
| step_limit | `workspace_member` | `first 12 steps` | 0 |

## Behavior

This flow starts at `workspace_member` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
