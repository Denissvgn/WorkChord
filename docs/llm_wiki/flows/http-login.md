# login

**Entry point:** `login` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [config](../modules/config.md), [identity_service](../modules/identity_service.md), [routers_identity](../modules/routers_identity.md), [session_service](../modules/session_service.md), [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as login
    participant p1 as IdentityService(…).begin_login
    participant p2 as IdentityService
    participant p3 as RedirectResponse
    participant p4 as _cookie_options
    participant p5 as response.set_cookie
    participant p6 as request.cookies.get
    participant p7 as get_settings
    participant p8 as _get_session_by_token
    participant p9 as _SESSION_TOKEN_PATTERN.fullmatch
    participant p10 as db.execute
    participant p11 as select(…).where
    participant p12 as select
    participant p13 as _token_digest
    participant p14 as result.scalar_one_or_none
    participant p15 as as_utc
    participant p16 as utc_now
    participant p17 as Settings
    participant p18 as hashlib.sha256(…).hexdigest
    participant p19 as value.replace
    participant p20 as datetime.now
    participant p21 as hashlib.sha256
    participant p22 as value.astimezone
    participant p23 as token.encode
    p0-->>p1: IdentityService(…).begin_login(return_to)
    p0->>p2: IdentityService
    p0-->>p3: RedirectResponse(url, status_code=303, headers={...})
    p0->>p4: _cookie_options
    p0-->>p5: response.set_cookie('workchord_login', browser, max_age=600, httponly=True, secure=options[...], samesite='lax', path=options[...])
    p0-->>p6: request.cookies.get(...)
    p0->>p7: get_settings
    p0->>p8: _get_session_by_token
    p0-->>p5: response.set_cookie('workchord_guest_transfer', guest, max_age=600, httponly=True, secure=options[...], samesite='lax', path=options[...])
    p4->>p7: get_settings
    p8-->>p9: _SESSION_TOKEN_PATTERN.fullmatch(token)
    p8-->>p10: db.execute(...)
    p8-->>p11: select(…).where(...)
    p8-->>p12: select(UserSession)
    p8->>p13: _token_digest
    p8-->>p14: result.scalar_one_or_none
    p8->>p15: as_utc
    p8->>p16: utc_now
    p7->>p17: Settings
    p13-->>p18: hashlib.sha256(…).hexdigest
    p15-->>p19: value.replace(tzinfo=UTC)
    p16-->>p20: datetime.now(UTC)
    p13-->>p21: hashlib.sha256(token.encode(...))
    p15-->>p22: value.astimezone(UTC)
    p13-->>p23: token.encode('utf-8')
```

> Call sequence diagram shows 25 of 25 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 4 of 4 (0 omitted); unresolved 12 of 12 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 10; effect analysis evaluated: 8, partial: 0, unavailable: 2. Counts include steps omitted from the displayed trace.

Collector observations for 8 source steps with known totals: observed: 23, emitted: 23, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `login` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `IdentityService(…).begin_login` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `IdentityService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `RedirectResponse` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_cookie_options` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `response.set_cookie` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `request.cookies.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `_get_session_by_token` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `_SESSION_TOKEN_PATTERN.fullmatch` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. login"]
    s2["2. IdentityService(…).begin_login"]
    s3["3. IdentityService"]
    s4["4. RedirectResponse"]
    s5["5. _cookie_options"]
    s6["6. get_settings"]
    s7["7. Settings"]
    s8["8. response.set_cookie"]
    s9["9. request.cookies.get"]
    s10["10. get_settings"]
    s11["11. _get_session_by_token"]
    s12["12. _SESSION_TOKEN_PATTERN.fullmatch"]
    s1 -. "IdentityService(…).begin_login(return_to)" .-> s2
    s1 -->|"IdentityService(db)"| s3
    s1 -. "RedirectResponse(url, status_code=303, headers={...})" .-> s4
    s1 -->|"_cookie_options(data not statically known)"| s5
    s5 -->|"get_settings(data not statically known)"| s6
    s6 -->|"Settings(data not statically known)"| s7
    s1 -. "response.set_cookie('workchord_login', browser, max_age=600, httponly=True, secure=options[...], samesite='lax', path=options[...])" .-> s8
    s1 -. "request.cookies.get(...)" .-> s9
    s1 -->|"get_settings(data not statically known)"| s10
    s1 -->|"_get_session_by_token(db, guest)"| s11
    s11 -. "_SESSION_TOKEN_PATTERN.fullmatch(token)" .-> s12
    click s1 "../modules/routers_identity.md"
    click s3 "../modules/identity_service.md"
    click s5 "../modules/session_service.md"
    click s6 "../modules/config.md"
    click s7 "../modules/config.md"
    click s10 "../modules/config.md"
    click s11 "../modules/session_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `login` | `request: Request`, `db: Database`, `return_to: str` | - | - | `response` |
| `IdentityService(…).begin_login` | - | - | - | - |
| `IdentityService` | - | - | - | - |
| `RedirectResponse` | - | - | - | - |
| `_cookie_options` | - | - | - | `{...}` |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `response.set_cookie` | - | - | - | - |
| `request.cookies.get` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `_get_session_by_token` | `db: AsyncSession`, `token: str \| None` | `UserSession` | - | `None`, `None`, `None`, `session` |
| `_SESSION_TOKEN_PATTERN.fullmatch` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| login | IdentityService(…).begin_login | 152 | `IdentityService(db).begin_login(return_to)` |
| login | IdentityService | 152 | `IdentityService(db)` |
| login | RedirectResponse | 153 | `RedirectResponse(url, status_code=303, headers={...})` |
| login | _cookie_options | 154 | `_cookie_options(data not statically known)` |
| _cookie_options | get_settings | 37 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| login | response.set_cookie | 155 | `response.set_cookie('workchord_login', browser, max_age=600, httponly=True, secure=options[...], samesite='lax', path=options[...])` |
| login | request.cookies.get | 156 | `request.cookies.get(...)` |
| login | get_settings | 156 | `get_settings(data not statically known)` |
| login | _get_session_by_token | 158 | `_get_session_by_token(db, guest)` |
| _get_session_by_token | _SESSION_TOKEN_PATTERN.fullmatch | 73 | `_SESSION_TOKEN_PATTERN.fullmatch(token)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `login` | `IdentityService(db).begin_login` | 152 |
| external_call | `login` | `RedirectResponse` | 153 |
| unresolved_call | `login` | `response.set_cookie` | 155 |
| unresolved_call | `login` | `request.cookies.get` | 156 |
| unresolved_call | `_get_session_by_token` | `_SESSION_TOKEN_PATTERN.fullmatch` | 73 |
| step_limit | `login` | `first 12 steps` | 0 |

## Behavior

This flow starts at `login` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

Starts trusted OIDC sign-in using browser state, nonce and PKCE. The response redirects to the configured provider and permits only a safe application return path.
