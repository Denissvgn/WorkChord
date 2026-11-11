# callback

**Entry point:** `callback` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [config](../modules/config.md), [identity_service](../modules/identity_service.md), [routers_identity](../modules/routers_identity.md), [session_service](../modules/session_service.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as callback
    participant p1 as IdentityService(…).finish_login
    participant p2 as IdentityService
    participant p3 as request.cookies.get
    participant p4 as get_client_ip
    participant p5 as request.headers.get (backend/app/routers/identity.py:callback)
    participant p6 as RedirectResponse
    participant p7 as _cookie_options
    participant p8 as get_settings
    participant p9 as response.set_cookie
    participant p10 as response.delete_cookie
    participant p11 as ip_address
    participant p12 as any
    participant p13 as ip_network
    participant p14 as request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)
    participant p15 as forwarded_for.split(…)[…].strip
    participant p16 as forwarded_for.split
    participant p17 as real_ip.strip
    participant p18 as Settings
    p0-->>p1: IdentityService(…).finish_login(code, state, request.cookies.get(...), ip_address=..., user_agent=request.headers.get(...))
    p0->>p2: IdentityService
    p0-->>p3: request.cookies.get('workchord_login')
    p0->>p4: get_client_ip
    p0-->>p5: request.headers.get (backend/app/routers/identity.py:callback)('User-Agent')
    p0-->>p6: RedirectResponse(target, status_code=303, headers={...})
    p0->>p7: _cookie_options
    p0->>p8: get_settings
    p0-->>p9: response.set_cookie(value=raw, **=options)
    p0-->>p10: response.delete_cookie('workchord_login', path=options[...], secure=options[...], httponly=True, samesite='lax')
    p4-->>p11: ip_address(direct_ip)
    p7->>p8: get_settings
    p4-->>p12: any(...)
    p4-->>p13: ip_network(network, strict=False)
    p4->>p8: get_settings
    p4-->>p14: request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)('X-Forwarded-For')
    p4-->>p15: forwarded_for.split(…)[…].strip
    p4-->>p16: forwarded_for.split(',')
    p4-->>p14: request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)('X-Real-IP')
    p4-->>p17: real_ip.strip
    p8->>p18: Settings
```

> Call sequence diagram shows 21 of 21 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 4 of 4 (0 omitted); unresolved 10 of 10 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 8; effect analysis evaluated: 6, partial: 0, unavailable: 2. Counts include steps omitted from the displayed trace.

Collector observations for 6 source steps with known totals: observed: 14, emitted: 14, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `callback` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `IdentityService(…).finish_login` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `IdentityService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `request.cookies.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `get_client_ip` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `ip_address` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `any` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `ip_network` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `forwarded_for.split(…)[…].strip` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. callback"]
    s2["2. IdentityService(…).finish_login"]
    s3["3. IdentityService"]
    s4["4. request.cookies.get"]
    s5["5. get_client_ip"]
    s6["6. ip_address"]
    s7["7. any"]
    s8["8. ip_network"]
    s9["9. get_settings"]
    s10["10. Settings"]
    s11["11. request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)"]
    s12["12. forwarded_for.split(…)[…].strip"]
    s1 -. "IdentityService(…).finish_login(code, state, request.cookies.get(...), ip_address=..., user_agent=request.headers.get(...))" .-> s2
    s1 -->|"IdentityService(db)"| s3
    s1 -. "request.cookies.get('workchord_login')" .-> s4
    s1 -->|"get_client_ip(request)"| s5
    s5 -. "ip_address(direct_ip)" .-> s6
    s5 -. "any(...)" .-> s7
    s5 -. "ip_network(network, strict=False)" .-> s8
    s5 -->|"get_settings(data not statically known)"| s9
    s9 -->|"Settings(data not statically known)"| s10
    s5 -. "request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)('X-Forwarded-For')" .-> s11
    s5 -. "forwarded_for.split(…)[…].strip(data not statically known)" .-> s12
    click s1 "../modules/routers_identity.md"
    click s3 "../modules/identity_service.md"
    click s5 "../modules/session_service.md"
    click s9 "../modules/config.md"
    click s10 "../modules/config.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `callback` | `request: Request`, `db: Database`, `code: str`, `state: str` | - | `options[...]` | `response` |
| `IdentityService(…).finish_login` | - | - | - | - |
| `IdentityService` | - | - | - | - |
| `request.cookies.get` | - | - | - | - |
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
| callback | IdentityService(…).finish_login | 200 | `IdentityService(db).finish_login(code, state, request.cookies.get(...), ip_address=..., user_agent=request.headers.get(...))` |
| callback | IdentityService | 200 | `IdentityService(db)` |
| callback | request.cookies.get | 200 | `request.cookies.get('workchord_login')` |
| callback | get_client_ip | 201 | `get_client_ip(request)` |
| get_client_ip | ip_address | 52 | `ip_address(direct_ip)` |
| get_client_ip | any | 53 | `any(...)` |
| get_client_ip | ip_network | 54 | `ip_network(network, strict=False)` |
| get_client_ip | get_settings | 55 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| get_client_ip | request.headers.get (backend/app/services/sess…n_service.py:get_client_ip) | 60 | `request.headers.get('X-Forwarded-For')` |
| get_client_ip | forwarded_for.split(…)[…].strip | 62 | `forwarded_for.split(',')[0].strip(data not statically known)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `callback` | `IdentityService(db).finish_login` | 200 |
| unresolved_call | `callback` | `request.cookies.get` | 200 |
| external_call | `get_client_ip` | `ip_address` | 52 |
| external_call | `get_client_ip` | `any` | 53 |
| external_call | `get_client_ip` | `ip_network` | 54 |
| unresolved_call | `get_client_ip` | `request.headers.get` | 60 |
| unresolved_call | `get_client_ip` | `forwarded_for.split(',')[0].strip` | 62 |
| step_limit | `callback` | `first 12 steps` | 0 |

## Behavior

This flow starts at `callback` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

Validates the provider response before issuing an opaque human session. Issuer/subject mapping determines the principal; matching IP, display name or profile ID does not establish identity.
