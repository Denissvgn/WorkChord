# me

**Entry point:** `me` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [app_maintenance](../modules/app_maintenance.md), [authority](../modules/authority.md), [commands](../modules/commands.md), and 8 more

**Complete modules touched:**

- [agent_service](../modules/agent_service.md)
- [app_maintenance](../modules/app_maintenance.md)
- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [http_authority](../modules/http_authority.md)
- [identity_service](../modules/identity_service.md)
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
    participant p2 as renewable_until
    participant p3 as local_work_profile
    participant p4 as get_settings
    participant p5 as session_lifetimes
    participant p6 as AgentService.authenticate
    participant p7 as IdentityService.actor_context
    participant p8 as admin_api_key_is_valid
    participant p9 as _get_session_by_token
    participant p10 as require_identity_writes
    participant p11 as IdentityService.context
    participant p12 as commit_or_flush
    participant p13 as as_utc
    participant p14 as internal_authority
    participant p15 as IdentityService
    participant p16 as AgentService
    participant p17 as AuthorityError
    participant p18 as Authority
    participant p19 as digest
    participant p20 as Settings
    participant p21 as hash_api_key
    participant p22 as _token_digest
    participant p23 as Principal
    participant p24 as utc_now
    participant p25 as current_command
    participant p26 as MaintenanceModeError
    participant p27 as bool
    participant p28 as db.get (backend/app/routers/identity.py:me)
    participant p29 as list
    p0->>p1: resolve_http_identity
    p0->>p2: renewable_until
    p0->>p3: local_work_profile
    p0->>p4: get_settings
    p2->>p5: session_lifetimes
    p1->>p6: AgentService.authenticate
    p1->>p7: IdentityService.actor_context
    p1->>p8: admin_api_key_is_valid
    p1->>p9: _get_session_by_token
    p7->>p10: require_identity_writes
    p7->>p11: IdentityService.context
    p6->>p12: commit_or_flush
    p2->>p13: as_utc
    p3->>p14: internal_authority
    p1->>p15: IdentityService
    p1->>p16: AgentService
    p1->>p17: AuthorityError
    p1->>p18: Authority
    p1->>p19: digest
    p4->>p20: Settings
    p6->>p21: hash_api_key
    p9->>p22: _token_digest
    p7->>p23: Principal
    p6->>p24: utc_now
    p12->>p25: current_command
    p10->>p26: MaintenanceModeError
    p0-->>p27: bool(...)
    p0-->>p28: db.get (backend/app/routers/identity.py:me)(UserSession, authority.session_id)
    p0-->>p29: list(SERVER_FEATURES)
    p0-->>p28: db.get (backend/app/routers/identity.py:me)(Principal, authority.principal_id)
```

> Call sequence diagram shows 30 of 147 interactions; 117 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 2 of 27 (25 omitted); unresolved 2 of 63 (61 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/http_authority.py:resolve_http_identity` | 2 | [backend/app/config.py](../modules/config.md) | internal | 1 |
| `backend/app/http_authority.py:resolve_http_identity` | 2 | - | unresolved | 27 |
| `backend/app/http_authority.py:resolve_http_identity` | 2 | [backend/app/authority.py](../modules/authority.md) | internal | 16 |
| `backend/app/authority.py:internal_authority` | 9 | - | unresolved | 1 |
| `backend/app/services/agent_service.py:hash_api_key` | 12 | - | unresolved | 2 |
| `backend/app/services/agent_service.py:hash_api_key` | 12 | - | external | 1 |
| `backend/app/services/agent_service.py:AgentService.authenticate` | 11 | - | unresolved | 5 |
| `backend/app/services/agent_service.py:AgentService.authenticate` | 11 | - | external | 2 |
> Omission summary shows 8 of 39 groups; 31 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 58; effect analysis evaluated: 34, partial: 0, unavailable: 24. Counts include steps omitted from the displayed trace.

Collector observations for 34 source steps with known totals: observed: 129, emitted: 129, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `me` | `available` | `evaluated` | `available` | `16` | `16` | `0` |
| `resolve_http_identity` | `available` | `evaluated` | `available` | `15` | `15` | `0` |
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
    b7["mutation contexts.append"]
    s2 -. "mutation contexts.append" .-> b7
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
    class b7 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `me` | `request: Request`, `response: Response`, `db: Database` | `AuthorityError`, `SERVER_FEATURES`, `UserSession`, `Principal`, `UserSession` | `response.headers[...]`, `result[...]`, `result[...]`, `result[...]`, `result[...]`, `result[...]` | `result` |
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
| me | resolve_http_identity | 164 | `resolve_http_identity(request, db)` |
| resolve_http_identity | get_settings | 53 | `get_settings(data not statically known)` |
| get_settings | Settings | 528 | `Settings(data not statically known)` |
| resolve_http_identity | IdentityService | 55 | `IdentityService(db)` |
| resolve_http_identity | request.headers.get | 56 | `request.headers.get('X-Agent-API-Key')` |
| resolve_http_identity | request.headers.get | 57 | `request.headers.get('X-Admin-API-Key')` |
| resolve_http_identity | request.headers.get | 58 | `request.headers.get('Authorization')` |
| resolve_http_identity | internal_authority | 59 | `internal_authority(db)` |
| internal_authority | db.info.get | 114 | `db.info.get('authority_internal', False)` |
| resolve_http_identity | AgentService.authenticate | 62 | `AgentService(db).authenticate(agent_key, touch=False)` |
| AgentService.authenticate | hash_api_key | 146 | `hash_api_key(api_key)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `result.update` | `me` | 183 |
| mutation | `contexts.append` | `resolve_http_identity` | 73 |
| mutation | `contexts.append` | `resolve_http_identity` | 75 |
| mutation | `contexts.append` | `resolve_http_identity` | 85 |
| mutation | `tokens.append` | `resolve_http_identity` | 97 |
| mutation | `tokens.append` | `resolve_http_identity` | 106 |
| mutation | `contexts.append` | `resolve_http_identity` | 118 |
| mutation | `contexts.append` | `resolve_http_identity` | 120 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `resolve_http_identity` | `request.headers.get` | 56 |
| unresolved_call | `resolve_http_identity` | `request.headers.get` | 57 |
| unresolved_call | `resolve_http_identity` | `request.headers.get` | 58 |
| unresolved_call | `internal_authority` | `db.info.get` | 114 |
| step_limit | `me` | `first 12 steps` | 0 |

## Behavior

Reports the access mode, the resolved principal and memberships, and for any session its access level. An observer also receives its client label, expiry and `renewable_until`. Authentication errors other than conflicting credentials are reported without failing the request. It always lists the server's `features`, so a client without a credential can choose which reads and pairing to use.
