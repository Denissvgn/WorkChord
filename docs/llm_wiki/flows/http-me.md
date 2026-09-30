# me

**Entry point:** `me` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [authority](../modules/authority.md), [config](../modules/config.md), [http_authority](../modules/http_authority.md), and 5 more

**Complete modules touched:**

- [agent_service](../modules/agent_service.md)
- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [http_authority](../modules/http_authority.md)
- [identity_service](../modules/identity_service.md)
- [routers_identity](../modules/routers_identity.md)
- [security](../modules/security.md)
- [session_service](../modules/session_service.md)
- [time](../modules/time.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as me
    participant p1 as resolve_http_identity
    participant p2 as get_settings
    participant p3 as Settings
    participant p4 as IdentityService
    participant p5 as request.headers.get
    participant p6 as internal_authority
    participant p7 as db.info.get
    participant p8 as AgentService(…).authenticate
    participant p9 as AgentService
    participant p10 as secrets.compare_digest (backend/app/http_authority.py:resolve_http_identity)
    participant p11 as request.url.path.removeprefix
    participant p12 as relative.startswith
    participant p13 as AuthorityError
    participant p14 as db.get (backend/app/http_authority.py:resolve_http_identity)
    participant p15 as contexts.append
    participant p16 as Authority
    participant p17 as identity.actor_context
    participant p18 as admin_api_key_is_valid
    participant p19 as secrets.compare_digest (backend/app/security.py:admin_api_key_is_valid)
    p0->>p1: resolve_http_identity
    p1->>p2: get_settings
    p2->>p3: Settings
    p1->>p4: IdentityService
    p1-->>p5: request.headers.get
    p1-->>p5: request.headers.get
    p1-->>p5: request.headers.get
    p1->>p6: internal_authority
    p6-->>p7: db.info.get
    p1-->>p8: AgentService(…).authenticate
    p1->>p9: AgentService
    p1-->>p10: secrets.compare_digest (backend/app/http_authority.py:resolve_http_identity)
    p1-->>p11: request.url.path.removeprefix
    p1-->>p12: relative.startswith
    p1->>p13: AuthorityError
    p1-->>p14: db.get (backend/app/http_authority.py:resolve_http_identity)
    p1-->>p14: db.get (backend/app/http_authority.py:resolve_http_identity)
    p1->>p13: AuthorityError
    p1-->>p15: contexts.append
    p1->>p16: Authority
    p1-->>p15: contexts.append
    p1-->>p17: identity.actor_context
    p1->>p18: admin_api_key_is_valid
    p18->>p2: get_settings
    p18-->>p19: secrets.compare_digest (backend/app/security.py:admin_api_key_is_valid)
    p1->>p13: AuthorityError
    p1-->>p14: db.get (backend/app/http_authority.py:resolve_http_identity)
    p1->>p13: AuthorityError
    p1-->>p14: db.get (backend/app/http_authority.py:resolve_http_identity)
    p1->>p13: AuthorityError
```

> Call sequence diagram shows 30 of 84 interactions; 54 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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
    s11["11. AgentService(…).authenticate"]
    s12["12. AgentService"]
    s1 -->|"resolve_http_identity(request, db)"| s2
    s2 -->|"get_settings(data not statically known)"| s3
    s3 -->|"Settings(data not statically known)"| s4
    s2 -->|"IdentityService(db)"| s5
    s2 -. "request.headers.get('X-Agent-API-Key')" .-> s6
    s2 -. "request.headers.get('X-Admin-API-Key')" .-> s7
    s2 -. "request.headers.get('Authorization')" .-> s8
    s2 -->|"internal_authority(db)"| s9
    s9 -. "db.info.get('authority_internal', False)" .-> s10
    s2 -. "AgentService(…).authenticate(agent_key, touch=False)" .-> s11
    s2 -->|"AgentService(db)"| s12
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
| `AgentService(…).authenticate` | - | - | - | - |
| `AgentService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| me | resolve_http_identity | 55 | `resolve_http_identity(request, db)` |
| resolve_http_identity | get_settings | 39 | `get_settings(data not statically known)` |
| get_settings | Settings | 479 | `Settings(data not statically known)` |
| resolve_http_identity | IdentityService | 41 | `IdentityService(db)` |
| resolve_http_identity | request.headers.get | 42 | `request.headers.get('X-Agent-API-Key')` |
| resolve_http_identity | request.headers.get | 43 | `request.headers.get('X-Admin-API-Key')` |
| resolve_http_identity | request.headers.get | 44 | `request.headers.get('Authorization')` |
| resolve_http_identity | internal_authority | 45 | `internal_authority(db)` |
| internal_authority | db.info.get | 87 | `db.info.get('authority_internal', False)` |
| resolve_http_identity | AgentService(…).authenticate | 48 | `AgentService(db).authenticate(agent_key, touch=False)` |
| resolve_http_identity | AgentService | 48 | `AgentService(db)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `result.update` | `me` | 66 |
| mutation | `contexts.append` | `resolve_http_identity` | 59 |
| mutation | `contexts.append` | `resolve_http_identity` | 61 |
| mutation | `contexts.append` | `resolve_http_identity` | 71 |
| mutation | `tokens.append` | `resolve_http_identity` | 82 |
| mutation | `tokens.append` | `resolve_http_identity` | 90 |
| mutation | `contexts.append` | `resolve_http_identity` | 95 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `resolve_http_identity` | `request.headers.get` | 42 |
| unresolved_call | `resolve_http_identity` | `request.headers.get` | 43 |
| unresolved_call | `resolve_http_identity` | `request.headers.get` | 44 |
| unresolved_call | `internal_authority` | `db.info.get` | 87 |
| unresolved_call | `resolve_http_identity` | `AgentService(db).authenticate` | 48 |
| step_limit | `me` | `first 12 steps` | 0 |

## Behavior

This flow starts at `me` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
