# task_owner_options

**Entry point:** `task_owner_options` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [authority](../modules/authority.md), [config](../modules/config.md), [routers_task_domain](../modules/routers_task_domain.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as task_owner_options
    participant p1 as require_project
    participant p2 as internal_authority
    participant p3 as get_settings
    participant p4 as AuthorityError
    participant p5 as Settings
    participant p6 as select
    participant p7 as select(…).where (backend/app/routers/task_…n.py:task_owner_options, 1)
    participant p8 as TeamMemberProfile.display_name.label
    participant p9 as db.info.get (backend/app/routers/task_…main.py:task_owner_options)
    participant p10 as select(…).where (backend/app/routers/task_…main.py:task_owner_options)
    participant p11 as ProjectMembership.role.in_
    participant p12 as select(…).where (backend/app/routers/task_…n.py:task_owner_options, 2)
    participant p13 as WorkspaceMembership.role.in_
    participant p14 as query.join(…).join(…).where
    participant p15 as query.join(…).join
    participant p16 as query.join
    participant p17 as Principal.enabled.is_
    participant p18 as or_
    participant p19 as Principal.id.in_
    participant p20 as (…).mappings().all
    participant p21 as (…).mappings
    participant p22 as db.execute
    participant p23 as query.order_by(…).limit
    participant p24 as query.order_by
    participant p25 as dict
    participant p26 as len
    p0->>p1: require_project
    p0->>p2: internal_authority
    p1->>p3: get_settings
    p1->>p4: AuthorityError
    p3->>p5: Settings
    p0-->>p6: select(TeamMemberProfile.id, TeamMemberProfile.display_name.label(...))
    p0-->>p7: select(…).where (backend/app/routers/task_…n.py:task_owner_options, 1)(..., ...)
    p0-->>p8: TeamMemberProfile.display_name.label('name')
    p0-->>p9: db.info.get (backend/app/routers/task_…main.py:task_owner_options)('authority')
    p0-->>p10: select(…).where (backend/app/routers/task_…main.py:task_owner_options)(..., ProjectMembership.role.in_(...))
    p0-->>p6: select(ProjectMembership.principal_id)
    p0-->>p11: ProjectMembership.role.in_([...])
    p0-->>p12: select(…).where (backend/app/routers/task_…n.py:task_owner_options, 2)(WorkspaceMembership.role.in_(...))
    p0-->>p6: select(WorkspaceMembership.principal_id)
    p0-->>p13: WorkspaceMembership.role.in_([...])
    p0-->>p14: query.join(…).join(…).where(Principal.enabled.is_(...), ..., or_(...))
    p0-->>p15: query.join(…).join(Principal, ...)
    p0-->>p16: query.join(PrincipalProfileLink, ...)
    p0-->>p17: Principal.enabled.is_(True)
    p0-->>p18: or_(Principal.id.in_(...), Principal.id.in_(...))
    p0-->>p19: Principal.id.in_(project_member)
    p0-->>p19: Principal.id.in_(workspace_member)
    p0-->>p20: (…).mappings().all
    p0-->>p21: (…).mappings
    p0-->>p22: db.execute(...)
    p0-->>p23: query.order_by(…).limit(...)
    p0-->>p24: query.order_by(TeamMemberProfile.id)
    p0-->>p25: dict(row)
    p0-->>p26: len(rows)
    p0-->>p26: len(rows)
```

> Call sequence diagram shows 30 of 34 interactions; 4 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 7 of 7 (0 omitted); unresolved 18 of 21 (3 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/authority.py:require_project` | 2 | - | unresolved | 2 |
| `backend/app/authority.py:require_project` | 2 | [backend/app/authority.py](../modules/authority.md) | internal | 1 |
| `backend/app/authority.py:internal_authority` | 26 | - | unresolved | 1 |
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 7; effect analysis evaluated: 4, partial: 0, unavailable: 3. Counts include steps omitted from the displayed trace.

Collector observations for 4 source steps with known totals: observed: 13, emitted: 13, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `task_owner_options` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `require_project` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `db.info.get (backend/app/authority.py:require_project)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `authority.allows` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `select(…).where (backend/app/routers/task_…n.py:task_owner_options, 1)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `TeamMemberProfile.display_name.label` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `db.info.get (backend/app/routers/task_…main.py:task_owner_options)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. task_owner_options"]
    s2["2. require_project"]
    s3["3. db.info.get (backend/app/authority.py:require_project)"]
    s4["4. get_settings"]
    s5["5. Settings"]
    s6["6. AuthorityError"]
    s7["7. authority.allows"]
    s8["8. AuthorityError"]
    s9["9. select(…).where (backend/app/routers/task_…n.py:task_owner_options, 1)"]
    s10["10. select"]
    s11["11. TeamMemberProfile.display_name.label"]
    s12["12. db.info.get (backend/app/routers/task_…main.py:task_owner_options)"]
    s1 -->|"require_project(db, project_id)"| s2
    s2 -. "db.info.get (backend/app/authority.py:require_project)('authority')" .-> s3
    s2 -->|"get_settings(data not statically known)"| s4
    s4 -->|"Settings(data not statically known)"| s5
    s2 -->|"AuthorityError('authentication_required', 'Sign in to continue.', 401)"| s6
    s2 -. "authority.allows(project_id, action)" .-> s7
    s2 -->|"AuthorityError(data not statically known)"| s8
    s1 -. "select(…).where (backend/app/routers/task_…n.py:task_owner_options, 1)(..., ...)" .-> s9
    s1 -. "select(TeamMemberProfile.id, TeamMemberProfile.display_name.label(...))" .-> s10
    s1 -. "TeamMemberProfile.display_name.label('name')" .-> s11
    s1 -. "db.info.get (backend/app/routers/task_…main.py:task_owner_options)('authority')" .-> s12
    click s1 "../modules/routers_task_domain.md"
    click s2 "../modules/authority.md"
    click s4 "../modules/config.md"
    click s5 "../modules/config.md"
    click s6 "../modules/authority.md"
    click s8 "../modules/authority.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `task_owner_options` | `db: DB`, `project_id: int \| None`, `after_id: int`, `limit: int` | - | - | `{...}` |
| `require_project` | `db`, `project_id`, `action` | - | - | `none` |
| `db.info.get (backend/app/authority.py:require_project)` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `authority.allows` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `select(…).where (backend/app/routers/task_…n.py:task_owner_options, 1)` | - | - | - | - |
| `select` | - | - | - | - |
| `TeamMemberProfile.display_name.label` | - | - | - | - |
| `db.info.get (backend/app/routers/task_…main.py:task_owner_options)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| task_owner_options | require_project | 146 | `require_project(db, project_id)` |
| require_project | db.info.get (backend/app/authority.py:require_project) | 69 | `db.info.get('authority')` |
| require_project | get_settings | 71 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| require_project | AuthorityError | 73 | `AuthorityError('authentication_required', 'Sign in to continue.', 401)` |
| require_project | authority.allows | 74 | `authority.allows(project_id, action)` |
| require_project | AuthorityError | 75 | `AuthorityError(data not statically known)` |
| task_owner_options | select(…).where (backend/app/routers/task_…n.py:task_owner_options, 1) | 147 | `select(TeamMemberProfile.id, TeamMemberProfile.display_name.label('name')).where(..., ...)` |
| task_owner_options | select | 147 | `select(TeamMemberProfile.id, TeamMemberProfile.display_name.label(...))` |
| task_owner_options | TeamMemberProfile.display_name.label | 147 | `TeamMemberProfile.display_name.label('name')` |
| task_owner_options | db.info.get (backend/app/routers/task_…main.py:task_owner_options) | 148 | `db.info.get('authority')` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `require_project` | `db.info.get` | 69 |
| unresolved_call | `require_project` | `authority.allows` | 74 |
| unresolved_call | `task_owner_options` | `select(TeamMemberProfile.id, TeamMemberProfile.display_name.label('name')).where` | 147 |
| external_call | `task_owner_options` | `select` | 147 |
| unresolved_call | `task_owner_options` | `TeamMemberProfile.display_name.label` | 147 |
| unresolved_call | `task_owner_options` | `db.info.get` | 148 |
| step_limit | `task_owner_options` | `first 12 steps` | 0 |

## Behavior

This flow starts at `task_owner_options` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
