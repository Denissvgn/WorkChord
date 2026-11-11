# me

**Entry point:** `me` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [authority](../modules/authority.md), [commands](../modules/commands.md), [config](../modules/config.md), and 8 more

**Complete modules touched:**

- [agent_service](../modules/agent_service.md)
- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [http_authority](../modules/http_authority.md)
- [identity_service](../modules/identity_service.md)
- [maintenance](../modules/maintenance.md)
- [models_identity](../modules/models_identity.md)
- [routers_identity](../modules/routers_identity.md)
- [security](../modules/security.md)
- [session_service](../modules/session_service.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as me
    participant p1 as resolve_http_identity
    participant p2 as get_settings
    participant p3 as AgentService.authenticate
    participant p4 as IdentityService.actor_context
    participant p5 as admin_api_key_is_valid
    participant p6 as _get_session_by_token
    participant p7 as require_identity_writes
    participant p8 as IdentityService.context
    participant p9 as commit_or_flush
    participant p10 as IdentityService
    participant p11 as internal_authority
    participant p12 as AgentService
    participant p13 as AuthorityError
    participant p14 as Authority
    participant p15 as digest
    participant p16 as Settings
    participant p17 as hash_api_key
    participant p18 as _token_digest
    participant p19 as Principal
    participant p20 as as_utc
    participant p21 as utc_now
    participant p22 as current_command
    participant p23 as MaintenanceModeError
    participant p24 as bool
    participant p25 as db.get (backend/app/routers/identity.py:me)
    participant p26 as result.update
    participant p27 as request.headers.get
    p0->>p1: resolve_http_identity
    p0->>p2: get_settings
    p1->>p3: AgentService.authenticate
    p1->>p4: IdentityService.actor_context
    p1->>p5: admin_api_key_is_valid
    p1->>p6: _get_session_by_token
    p4->>p7: require_identity_writes
    p4->>p8: IdentityService.context
    p3->>p9: commit_or_flush
    p1->>p10: IdentityService
    p1->>p11: internal_authority
    p1->>p12: AgentService
    p1->>p13: AuthorityError
    p1->>p14: Authority
    p1->>p15: digest
    p2->>p16: Settings
    p3->>p17: hash_api_key
    p6->>p18: _token_digest
    p4->>p19: Principal
    p6->>p20: as_utc
    p3->>p21: utc_now
    p9->>p22: current_command
    p7->>p23: MaintenanceModeError
    p0-->>p24: bool(...)
    p0-->>p25: db.get (backend/app/routers/identity.py:me)(Principal, authority.principal_id)
    p0-->>p26: result.update(principal={...}, workspace_role=authority.workspace_role, projects=authority.projects)
    p0-->>p25: db.get (backend/app/routers/identity.py:me)(TeamMemberProfile, authority.profile_id)
    p0-->>p25: db.get (backend/app/routers/identity.py:me)(UserSession, authority.session_id)
    p1-->>p27: request.headers.get('X-Agent-API-Key')
    p1-->>p27: request.headers.get('X-Admin-API-Key')
```

> Call sequence diagram shows 30 of 130 interactions; 100 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 22 (21 omitted); unresolved 6 of 60 (54 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/http_authority.py:resolve_http_identity` | 2 | [backend/app/config.py](../modules/config.md) | internal | 1 |
| `backend/app/http_authority.py:resolve_http_identity` | 2 | - | unresolved | 24 |
| `backend/app/authority.py:internal_authority` | 9 | - | unresolved | 1 |
| `backend/app/services/agent_service.py:hash_api_key` | 12 | - | unresolved | 2 |
| `backend/app/services/agent_service.py:hash_api_key` | 12 | - | external | 1 |
| `backend/app/services/agent_service.py:AgentService.authenticate` | 11 | - | unresolved | 5 |
| `backend/app/services/agent_service.py:AgentService.authenticate` | 11 | - | external | 2 |
| `backend/app/services/agent_service.py:AgentService.authenticate` | 11 | [backend/app/config.py](../modules/config.md) | internal | 1 |
> Omission summary shows 8 of 35 groups; 27 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 49; effect analysis evaluated: 28, partial: 0, unavailable: 21. Counts include steps omitted from the displayed trace.

Collector observations for 28 source steps with known totals: observed: 105, emitted: 105, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `me` | `available` | `evaluated` | `available` | `11` | `11` | `0` |
| `resolve_http_identity` | `available` | `evaluated` | `available` | `14` | `14` | `0` |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `IdentityService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `request.headers.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `request.headers.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `request.headers.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `internal_authority` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `db.info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AgentService.authenticate` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `hash_api_key` | `available` | `evaluated` | `available` | `2` | `2` | `0` |

```mermaid
flowchart LR
    s1["1. me"]
    s2["2. resolve_http_identity"]
    s3["3. get_settings"]
    s4["4. Settings"]
    s5["5. IdentityService"]
    s6["6. request.headers.get"]
    s7["7. request.headers.get"]
    s8["8. request.headers.get"]
    s9["9. internal_authority"]
    s10["10. db.info.get"]
    s11["11. AgentService.authenticate"]
    s12["12. hash_api_key"]
    s1 -->|"resolve_http_identity(request, db)"| s2
    s2 -->|"get_settings(data not statically known)"| s3
    s3 -->|"Settings(data not statically known)"| s4
    s2 -->|"IdentityService(db)"| s5
    s2 -. "request.headers.get('X-Agent-API-Key')" .-> s6
    s2 -. "request.headers.get('X-Admin-API-Key')" .-> s7
    s2 -. "request.headers.get('Authorization')" .-> s8
    s2 -->|"internal_authority(db)"| s9
    s9 -. "db.info.get('authority_internal', False)" .-> s10
    s2 -->|"AgentService.authenticate(agent_key, touch=False)"| s11
    s11 -->|"hash_api_key(api_key)"| s12
    b0["mutation result.update"]
    s1 -. "mutation result.update" .-> b0
    b1["mutation contexts.append"]
    s2 -. "mutation contexts.append" .-> b1
    b2["mutation contexts.append"]
    s2 -. "mutation contexts.append" .-> b2
    b3["mutation contexts.append"]
    s2 -. "mutation contexts.append" .-> b3
    b4["mutation tokens.append"]
    s2 -. "mutation tokens.append" .-> b4
    b5["mutation tokens.append"]
    s2 -. "mutation tokens.append" .-> b5
    b6["mutation contexts.append"]
    s2 -. "mutation contexts.append" .-> b6
    click s1 "../modules/routers_identity.md"
    click s2 "../modules/http_authority.md"
    click s3 "../modules/config.md"
    click s4 "../modules/config.md"
    click s5 "../modules/identity_service.md"
    click s9 "../modules/authority.md"
    click s11 "../modules/agent_service.md"
    click s12 "../modules/agent_service.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
    class b4 boundary
    class b5 boundary
    class b6 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `me` | `request: Request`, `response: Response`, `db: Database` | `AuthorityError`, `Principal`, `UserSession` | `response.headers[...]`, `result[...]`, `result[...]` | `result` |
| `resolve_http_identity` | `request`, `db` | `WorkspaceAuthorityState`, `Principal`, `WorkspaceAuthorityState`, `Principal`, `Principal` | - | `authority` |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `IdentityService` | - | - | - | - |
| `request.headers.get` | - | - | - | - |
| `request.headers.get` | - | - | - | - |
| `request.headers.get` | - | - | - | - |
| `internal_authority` | `db` | - | `db.info[...]`, `db.info[...]` | - |
| `db.info.get` | - | - | - | - |
| `AgentService.authenticate` | `api_key: str`, `touch: bool` | `AgentActor`, `AgentActor`, `self.db` | `actor.last_seen_at` | `actor` |
| `hash_api_key` | `api_key: str` | - | - | `...` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| me | resolve_http_identity | 127 | `resolve_http_identity(request, db)` |
| resolve_http_identity | get_settings | 42 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| resolve_http_identity | IdentityService | 44 | `IdentityService(db)` |
| resolve_http_identity | request.headers.get | 45 | `request.headers.get('X-Agent-API-Key')` |
| resolve_http_identity | request.headers.get | 46 | `request.headers.get('X-Admin-API-Key')` |
| resolve_http_identity | request.headers.get | 47 | `request.headers.get('Authorization')` |
| resolve_http_identity | internal_authority | 48 | `internal_authority(db)` |
| internal_authority | db.info.get | 87 | `db.info.get('authority_internal', False)` |
| resolve_http_identity | AgentService.authenticate | 51 | `AgentService(db).authenticate(agent_key, touch=False)` |
| AgentService.authenticate | hash_api_key | 133 | `hash_api_key(api_key)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `result.update` | `me` | 138 |
| mutation | `contexts.append` | `resolve_http_identity` | 62 |
| mutation | `contexts.append` | `resolve_http_identity` | 64 |
| mutation | `contexts.append` | `resolve_http_identity` | 74 |
| mutation | `tokens.append` | `resolve_http_identity` | 85 |
| mutation | `tokens.append` | `resolve_http_identity` | 93 |
| mutation | `contexts.append` | `resolve_http_identity` | 98 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `resolve_http_identity` | `request.headers.get` | 45 |
| unresolved_call | `resolve_http_identity` | `request.headers.get` | 46 |
| unresolved_call | `resolve_http_identity` | `request.headers.get` | 47 |
| unresolved_call | `internal_authority` | `db.info.get` | 87 |
| step_limit | `me` | `first 12 steps` | 0 |

## Behavior

This flow starts at `me` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
