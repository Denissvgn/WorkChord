# native_token

**Entry point:** `native_token` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [authority](../modules/authority.md), [config](../modules/config.md), [identity_service](../modules/identity_service.md), [routers_identity](../modules/routers_identity.md), and 1 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [identity_service](../modules/identity_service.md)
- [routers_identity](../modules/routers_identity.md)
- [session_service](../modules/session_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as native_token
    participant p1 as AuthorityError
    participant p2 as IdentityService(…).issue_session
    participant p3 as IdentityService
    participant p4 as get_client_ip
    participant p5 as ip_address
    participant p6 as any
    participant p7 as ip_network
    participant p8 as get_settings
    participant p9 as Settings
    participant p10 as request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)
    participant p11 as forwarded_for.split(…)[…].strip
    participant p12 as forwarded_for.split
    participant p13 as real_ip.strip
    participant p14 as request.headers.get (backend/app/routers/identity.py:native_token)
    p0->>p1: AuthorityError
    p0-->>p2: IdentityService(…).issue_session
    p0->>p3: IdentityService
    p0->>p4: get_client_ip
    p4-->>p5: ip_address
    p4-->>p6: any
    p4-->>p7: ip_network
    p4->>p8: get_settings
    p8->>p9: Settings
    p4-->>p10: request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)
    p4-->>p11: forwarded_for.split(…)[…].strip
    p4-->>p12: forwarded_for.split
    p4-->>p10: request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)
    p4-->>p13: real_ip.strip
    p0-->>p14: request.headers.get (backend/app/routers/identity.py:native_token)
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. native_token"]
    s2["2. AuthorityError"]
    s3["3. IdentityService(…).issue_session"]
    s4["4. IdentityService"]
    s5["5. get_client_ip"]
    s6["6. ip_address"]
    s7["7. any"]
    s8["8. ip_network"]
    s9["9. get_settings"]
    s10["10. Settings"]
    s11["11. request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)"]
    s12["12. forwarded_for.split(…)[…].strip"]
    s1 -->|"AuthorityError(data not statically known)"| s2
    s1 -. "IdentityService(…).issue_session(authority.principal_id, ..., request.headers.get(...))" .-> s3
    s1 -->|"IdentityService(db)"| s4
    s1 -->|"get_client_ip(request)"| s5
    s5 -. "ip_address(direct_ip)" .-> s6
    s5 -. "any(...)" .-> s7
    s5 -. "ip_network(network, strict=False)" .-> s8
    s5 -->|"get_settings(data not statically known)"| s9
    s9 -->|"Settings(data not statically known)"| s10
    s5 -. "request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)('X-Forwarded-For')" .-> s11
    s5 -. "forwarded_for.split(…)[…].strip(data not statically known)" .-> s12
    click s1 "../modules/routers_identity.md"
    click s2 "../modules/authority.md"
    click s4 "../modules/identity_service.md"
    click s5 "../modules/session_service.md"
    click s9 "../modules/config.md"
    click s10 "../modules/config.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `native_token` | `request: Request`, `response: Response`, `db: Database` | - | `response.headers[...]` | `{...}` |
| `AuthorityError` | - | - | - | - |
| `IdentityService(…).issue_session` | - | - | - | - |
| `IdentityService` | - | - | - | - |
| `get_client_ip` | `request: Request` | - | - | `...`, `real_ip.strip(...)`, `direct_ip` |
| `ip_address` | - | - | - | - |
| `any` | - | - | - | - |
| `ip_network` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)` | - | - | - | - |
| `forwarded_for.split(…)[…].strip` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| native_token | AuthorityError | 296 | `AuthorityError(data not statically known)` |
| native_token | IdentityService(…).issue_session | 297 | `IdentityService(db).issue_session(authority.principal_id, ..., request.headers.get(...))` |
| native_token | IdentityService | 297 | `IdentityService(db)` |
| native_token | get_client_ip | 297 | `get_client_ip(request)` |
| get_client_ip | ip_address | 52 | `ip_address(direct_ip)` |
| get_client_ip | any | 53 | `any(...)` |
| get_client_ip | ip_network | 54 | `ip_network(network, strict=False)` |
| get_client_ip | get_settings | 55 | `get_settings(data not statically known)` |
| get_settings | Settings | 480 | `Settings(data not statically known)` |
| get_client_ip | request.headers.get (backend/app/services/sess…n_service.py:get_client_ip) | 60 | `request.headers.get('X-Forwarded-For')` |
| get_client_ip | forwarded_for.split(…)[…].strip | 62 | `forwarded_for.split(',')[0].strip(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `native_token` | `IdentityService(db).issue_session` | 297 |
| external_call | `get_client_ip` | `ip_address` | 52 |
| external_call | `get_client_ip` | `any` | 53 |
| external_call | `get_client_ip` | `ip_network` | 54 |
| unresolved_call | `get_client_ip` | `request.headers.get` | 60 |
| unresolved_call | `get_client_ip` | `forwarded_for.split(',')[0].strip` | 62 |
| step_limit | `native_token` | `first 12 steps` | 0 |

## Behavior

This flow starts at `native_token` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
