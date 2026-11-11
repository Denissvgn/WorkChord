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

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as project_member
    participant p1 as authority.allows
    participant p2 as AuthorityError
    participant p3 as require_identity_writes
    participant p4 as internal_authority
    participant p5 as db.get
    participant p6 as db.delete
    participant p7 as db.add
    participant p8 as ProjectMembership
    participant p9 as CommandAudit
    participant p10 as db.flush
    participant p11 as get_settings
    participant p12 as db.info.get
    participant p13 as MaintenanceModeError
    participant p14 as Settings
    p0-->>p1: authority.allows(project_id, 'manage')
    p0->>p2: AuthorityError
    p0->>p3: require_identity_writes
    p0->>p2: AuthorityError
    p0->>p4: internal_authority
    p0-->>p5: db.get(Principal, principal_id)
    p0-->>p5: db.get(Project, project_id)
    p0->>p2: AuthorityError
    p0-->>p5: db.get(ProjectMembership, (...))
    p0-->>p6: db.delete(existing)
    p0-->>p7: db.add(ProjectMembership(...))
    p0->>p8: ProjectMembership
    p0-->>p7: db.add(CommandAudit(...))
    p0->>p9: CommandAudit
    p0-->>p10: db.flush
    p3->>p11: get_settings
    p4-->>p12: db.info.get('authority_internal', False)
    p3->>p13: MaintenanceModeError
    p3->>p11: get_settings
    p11->>p14: Settings
```

> Call sequence diagram shows 20 of 20 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 0 of 0 (0 omitted); unresolved 9 of 9 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 12; effect analysis evaluated: 5, partial: 0, unavailable: 7. Counts include steps omitted from the displayed trace.

Collector observations for 5 source steps with known totals: observed: 15, emitted: 15, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `project_member` | `available` | `evaluated` | `available` | `10` | `10` | `0` |
| `authority.allows` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `require_identity_writes` | `available` | `evaluated` | `available` | `0` | `0` | `0` |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `MaintenanceModeError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `internal_authority` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `db.info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `db.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

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
| project_member | authority.allows | 269 | `authority.allows(project_id, 'manage')` |
| project_member | AuthorityError | 270 | `AuthorityError(data not statically known)` |
| project_member | require_identity_writes | 271 | `require_identity_writes(data not statically known)` |
| require_identity_writes | get_settings | 31 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| require_identity_writes | MaintenanceModeError | 32 | `MaintenanceModeError(operation='identity lifecycle', mode=...)` |
| require_identity_writes | get_settings | 32 | `get_settings(data not statically known)` |
| project_member | AuthorityError | 273 | `AuthorityError('invalid_project_role', 'Choose a project role.', 422)` |
| project_member | internal_authority | 275 | `internal_authority(db)` |
| internal_authority | db.info.get | 87 | `db.info.get('authority_internal', False)` |
| project_member | db.get | 276 | `db.get(Principal, principal_id)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `db.add` | `project_member` | 285 |
| mutation | `db.add` | `project_member` | 286 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `project_member` | `authority.allows` | 269 |
| unresolved_call | `internal_authority` | `db.info.get` | 87 |
| unresolved_call | `project_member` | `db.get` | 276 |
| step_limit | `project_member` | `first 12 steps` | 0 |

## Behavior

This flow starts at `project_member` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
