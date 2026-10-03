# login

**Entry point:** `login` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [config](../modules/config.md), [identity_service](../modules/identity_service.md), [routers_identity](../modules/routers_identity.md), [session_service](../modules/session_service.md), [time](../modules/time.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as login
    participant p1 as IdentityService(…).begin_login
    participant p2 as IdentityService
    participant p3 as RedirectResponse
    participant p4 as _cookie_options
    participant p5 as get_settings
    participant p6 as Settings
    participant p7 as response.set_cookie
    participant p8 as request.cookies.get
    participant p9 as _get_session_by_token
    participant p10 as _SESSION_TOKEN_PATTERN.fullmatch
    participant p11 as db.execute
    participant p12 as select(…).where
    participant p13 as select
    participant p14 as _token_digest
    participant p15 as hashlib.sha256(…).hexdigest
    participant p16 as hashlib.sha256
    participant p17 as token.encode
    participant p18 as result.scalar_one_or_none
    participant p19 as as_utc
    participant p20 as value.replace
    participant p21 as value.astimezone
    participant p22 as utc_now
    participant p23 as datetime.now
    p0-->>p1: IdentityService(…).begin_login
    p0->>p2: IdentityService
    p0-->>p3: RedirectResponse
    p0->>p4: _cookie_options
    p4->>p5: get_settings
    p5->>p6: Settings
    p0-->>p7: response.set_cookie
    p0-->>p8: request.cookies.get
    p0->>p5: get_settings
    p0->>p9: _get_session_by_token
    p9-->>p10: _SESSION_TOKEN_PATTERN.fullmatch
    p9-->>p11: db.execute
    p9-->>p12: select(…).where
    p9-->>p13: select
    p9->>p14: _token_digest
    p14-->>p15: hashlib.sha256(…).hexdigest
    p14-->>p16: hashlib.sha256
    p14-->>p17: token.encode
    p9-->>p18: result.scalar_one_or_none
    p9->>p19: as_utc
    p19-->>p20: value.replace
    p19-->>p21: value.astimezone
    p9->>p22: utc_now
    p22-->>p23: datetime.now
    p0-->>p7: response.set_cookie
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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
| get_settings | Settings | 479 | `Settings(data not statically known)` |
| login | response.set_cookie | 155 | `response.set_cookie('workchord_login', browser, max_age=600, httponly=True, secure=options[...], samesite='lax', path=options[...])` |
| login | request.cookies.get | 156 | `request.cookies.get(...)` |
| login | get_settings | 156 | `get_settings(data not statically known)` |
| login | _get_session_by_token | 158 | `_get_session_by_token(db, guest)` |
| _get_session_by_token | _SESSION_TOKEN_PATTERN.fullmatch | 73 | `_SESSION_TOKEN_PATTERN.fullmatch(token)` |

### Boundary effects

*No boundary effects detected.*

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
