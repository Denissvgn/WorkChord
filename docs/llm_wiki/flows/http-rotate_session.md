# rotate_session

**Entry point:** `rotate_session` (`http`)
**Source:** [routers_session](../modules/routers_session.md)
**Modules touched:** [config](../modules/config.md), [routers_session](../modules/routers_session.md), [session_service](../modules/session_service.md), [time](../modules/time.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as rotate_session (backend/app/routers/session.py)
    participant p1 as rotate_session (backend/app/services/session_service.py)
    participant p2 as _new_token
    participant p3 as secrets.token_urlsafe
    participant p4 as _token_digest
    participant p5 as hashlib.sha256(…).hexdigest
    participant p6 as hashlib.sha256
    participant p7 as token.encode
    participant p8 as utc_now
    participant p9 as datetime.now
    participant p10 as timedelta
    participant p11 as get_settings
    participant p12 as Settings
    participant p13 as db.commit
    participant p14 as db.refresh
    participant p15 as response.set_cookie
    participant p16 as _cookie_options
    p0->>p1: rotate_session (backend/app/services/session_service.py)
    p1->>p2: _new_token
    p2-->>p3: secrets.token_urlsafe
    p1->>p4: _token_digest
    p4-->>p5: hashlib.sha256(…).hexdigest
    p4-->>p6: hashlib.sha256
    p4-->>p7: token.encode
    p1->>p8: utc_now
    p8-->>p9: datetime.now
    p1-->>p10: timedelta
    p1->>p11: get_settings
    p11->>p12: Settings
    p1-->>p13: db.commit
    p1-->>p14: db.refresh
    p1-->>p15: response.set_cookie
    p1->>p16: _cookie_options
    p16->>p11: get_settings
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. rotate_session (backend/app/routers/session.py)"]
    s2["2. rotate_session (backend/app/services/session_service.py)"]
    s3["3. _new_token"]
    s4["4. secrets.token_urlsafe"]
    s5["5. _token_digest"]
    s6["6. hashlib.sha256(…).hexdigest"]
    s7["7. hashlib.sha256"]
    s8["8. token.encode"]
    s9["9. utc_now"]
    s10["10. datetime.now"]
    s11["11. timedelta"]
    s12["12. get_settings"]
    s1 -->|"rotate_session (backend/app/services/session_service.py)(db, current_session, response)"| s2
    s2 -->|"_new_token(data not statically known)"| s3
    s3 -. "secrets.token_urlsafe(32)" .-> s4
    s2 -->|"_token_digest(raw_token)"| s5
    s5 -. "hashlib.sha256(…).hexdigest(data not statically known)" .-> s6
    s5 -. "hashlib.sha256(token.encode(...))" .-> s7
    s5 -. "token.encode('utf-8')" .-> s8
    s2 -->|"utc_now(data not statically known)"| s9
    s9 -. "datetime.now(UTC)" .-> s10
    s2 -. "timedelta(seconds=...)" .-> s11
    s2 -->|"get_settings(data not statically known)"| s12
    click s1 "../modules/routers_session.md"
    click s2 "../modules/session_service.md"
    click s3 "../modules/session_service.md"
    click s5 "../modules/session_service.md"
    click s9 "../modules/time.md"
    click s12 "../modules/config.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `rotate_session (backend/app/routers/session.py)` | `response: Response`, `current_session: Annotated[UserSession, Depends(session_service.get_current_session)]`, `db: Annotated[AsyncSession, Depends(get_db)]` | - | - | `...` |
| `rotate_session (backend/app/services/session_service.py)` | `db: AsyncSession`, `session: UserSession`, `response: Response` | - | `session.session_token_hash`, `session.expires_at`, `session.revoked_at` | `session` |
| `_new_token` | - | - | - | `secrets.token_urlsafe(...)` |
| `secrets.token_urlsafe` | - | - | - | - |
| `_token_digest` | `token: str` | - | - | `...` |
| `hashlib.sha256(…).hexdigest` | - | - | - | - |
| `hashlib.sha256` | - | - | - | - |
| `token.encode` | - | - | - | - |
| `utc_now` | - | `UTC` | - | `datetime.now(...)` |
| `datetime.now` | - | - | - | - |
| `timedelta` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| rotate_session (backend/app/routers/session.py) | rotate_session (backend/app/services/session_service.py) | 33 | `session_service.rotate_session(db, current_session, response)` |
| rotate_session (backend/app/services/session_service.py) | _new_token | 180 | `_new_token(data not statically known)` |
| _new_token | secrets.token_urlsafe | 31 | `secrets.token_urlsafe(32)` |
| rotate_session (backend/app/services/session_service.py) | _token_digest | 181 | `_token_digest(raw_token)` |
| _token_digest | hashlib.sha256(…).hexdigest | 27 | `hashlib.sha256(token.encode('utf-8')).hexdigest(data not statically known)` |
| _token_digest | hashlib.sha256 | 27 | `hashlib.sha256(token.encode(...))` |
| _token_digest | token.encode | 27 | `token.encode('utf-8')` |
| rotate_session (backend/app/services/session_service.py) | utc_now | 182 | `utc_now(data not statically known)` |
| utc_now | datetime.now | 13 | `datetime.now(UTC)` |
| rotate_session (backend/app/services/session_service.py) | timedelta | 182 | `timedelta(seconds=...)` |
| rotate_session (backend/app/services/session_service.py) | get_settings | 183 | `get_settings(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `_new_token` | `secrets.token_urlsafe` | 31 |
| unresolved_call | `_token_digest` | `hashlib.sha256(token.encode('utf-8')).hexdigest` | 27 |
| external_call | `_token_digest` | `hashlib.sha256` | 27 |
| unresolved_call | `_token_digest` | `token.encode` | 27 |
| external_call | `utc_now` | `datetime.now` | 13 |
| external_call | `rotate_session` | `timedelta` | 182 |
| step_limit | `rotate_session` | `first 12 steps` | 0 |

## Behavior

This flow starts at `rotate_session` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
