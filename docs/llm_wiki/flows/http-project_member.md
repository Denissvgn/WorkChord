# project_member

**Entry point:** `project_member` (`http`)
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
    participant p0 as project_member
    participant p1 as authority.allows
    participant p2 as AuthorityError
    participant p3 as require_identity_writes
    participant p4 as get_settings
    participant p5 as Settings
    participant p6 as MaintenanceModeError
    participant p7 as internal_authority
    participant p8 as db.info.get
    participant p9 as db.get
    participant p10 as db.delete
    participant p11 as db.add
    participant p12 as ProjectMembership
    participant p13 as CommandAudit
    participant p14 as db.flush
    p0-->>p1: authority.allows
    p0->>p2: AuthorityError
    p0->>p3: require_identity_writes
    p3->>p4: get_settings
    p4->>p5: Settings
    p3->>p6: MaintenanceModeError
    p3->>p4: get_settings
    p0->>p2: AuthorityError
    p0->>p7: internal_authority
    p7-->>p8: db.info.get
    p0-->>p9: db.get
    p0-->>p9: db.get
    p0->>p2: AuthorityError
    p0-->>p9: db.get
    p0-->>p10: db.delete
    p0-->>p11: db.add
    p0->>p12: ProjectMembership
    p0-->>p11: db.add
    p0->>p13: CommandAudit
    p0-->>p14: db.flush
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. project_member"]
    s2["2. authority.allows"]
    s3["3. AuthorityError"]
    s4["4. require_identity_writes"]
    s5["5. get_settings"]
    s6["6. Settings"]
    s7["7. MaintenanceModeError"]
    s8["8. get_settings"]
    s9["9. AuthorityError"]
    s10["10. internal_authority"]
    s11["11. db.info.get"]
    s12["12. db.get"]
    s1 -. "authority.allows(project_id, 'manage')" .-> s2
    s1 -->|"AuthorityError(data not statically known)"| s3
    s1 -->|"require_identity_writes(data not statically known)"| s4
    s4 -->|"get_settings(data not statically known)"| s5
    s5 -->|"Settings(data not statically known)"| s6
    s4 -->|"MaintenanceModeError(operation='identity lifecycle', mode=...)"| s7
    s4 -->|"get_settings(data not statically known)"| s8
    s1 -->|"AuthorityError('invalid_project_role', 'Choose a project role.', 422)"| s9
    s1 -->|"internal_authority(db)"| s10
    s10 -. "db.info.get('authority_internal', False)" .-> s11
    s1 -. "db.get(Principal, principal_id)" .-> s12
    b0["mutation db.add"]
    s1 -. "mutation db.add" .-> b0
    b1["mutation db.add"]
    s1 -. "mutation db.add" .-> b1
    click s1 "../modules/routers_identity.md"
    click s3 "../modules/authority.md"
    click s4 "../modules/identity_service.md"
    click s5 "../modules/config.md"
    click s6 "../modules/config.md"
    click s7 "../modules/maintenance.md"
    click s8 "../modules/config.md"
    click s9 "../modules/authority.md"
    click s10 "../modules/authority.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `project_member` | `project_id: int`, `principal_id: int`, `data: MembershipChange`, `db: Database` | `Principal`, `ProjectMembership` | `existing.role` | `{...}` |
| `authority.allows` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `require_identity_writes` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `MaintenanceModeError` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `AuthorityError` | - | - | - | - |
| `internal_authority` | `db` | - | `db.info[...]`, `db.info[...]` | - |
| `db.info.get` | - | - | - | - |
| `db.get` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| project_member | authority.allows | 235 | `authority.allows(project_id, 'manage')` |
| project_member | AuthorityError | 236 | `AuthorityError(data not statically known)` |
| project_member | require_identity_writes | 237 | `require_identity_writes(data not statically known)` |
| require_identity_writes | get_settings | 31 | `get_settings(data not statically known)` |
| get_settings | Settings | 479 | `Settings(data not statically known)` |
| require_identity_writes | MaintenanceModeError | 32 | `MaintenanceModeError(operation='identity lifecycle', mode=...)` |
| require_identity_writes | get_settings | 32 | `get_settings(data not statically known)` |
| project_member | AuthorityError | 239 | `AuthorityError('invalid_project_role', 'Choose a project role.', 422)` |
| project_member | internal_authority | 241 | `internal_authority(db)` |
| internal_authority | db.info.get | 87 | `db.info.get('authority_internal', False)` |
| project_member | db.get | 242 | `db.get(Principal, principal_id)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `db.add` | `project_member` | 251 |
| mutation | `db.add` | `project_member` | 252 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `project_member` | `authority.allows` | 235 |
| unresolved_call | `internal_authority` | `db.info.get` | 87 |
| unresolved_call | `project_member` | `db.get` | 242 |
| step_limit | `project_member` | `first 12 steps` | 0 |

## Behavior

This flow starts at `project_member` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
