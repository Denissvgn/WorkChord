# revoke_session

**Entry point:** `revoke_session` (`http`)
**Source:** [routers_session](../modules/routers_session.md)
**Modules touched:** [commands](../modules/commands.md), [config](../modules/config.md), [routers_session](../modules/routers_session.md), [schemas_common](../modules/schemas_common.md), and 2 more

**Complete modules touched:**

- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [routers_session](../modules/routers_session.md)
- [schemas_common](../modules/schemas_common.md)
- [session_service](../modules/session_service.md)
- [time](../modules/time.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as revoke_session (backend/app/routers/session.py)
    participant p1 as revoke_session (backend/app/services/session_service.py)
    participant p2 as utc_now
    participant p3 as datetime.now
    participant p4 as commit_or_flush
    participant p5 as current_command
    participant p6 as getattr
    participant p7 as isinstance
    participant p8 as info.get
    participant p9 as db.flush
    participant p10 as db.commit
    participant p11 as _cookie_options
    participant p12 as get_settings
    participant p13 as Settings
    participant p14 as response.delete_cookie
    participant p15 as MessageResponse
    p0->>p1: revoke_session (backend/app/services/session_service.py)
    p1->>p2: utc_now
    p2-->>p3: datetime.now
    p1->>p4: commit_or_flush
    p4->>p5: current_command
    p5-->>p6: getattr
    p5-->>p7: isinstance
    p5-->>p8: info.get
    p4-->>p9: db.flush
    p4-->>p10: db.commit
    p1->>p11: _cookie_options
    p11->>p12: get_settings
    p12->>p13: Settings
    p1-->>p14: response.delete_cookie
    p0->>p15: MessageResponse
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. revoke_session (backend/app/routers/session.py)"]
    s2["2. revoke_session (backend/app/services/session_service.py)"]
    s3["3. utc_now"]
    s4["4. datetime.now"]
    s5["5. commit_or_flush"]
    s6["6. current_command"]
    s7["7. getattr"]
    s8["8. isinstance"]
    s9["9. info.get"]
    s10["10. db.flush"]
    s11["11. db.commit"]
    s12["12. _cookie_options"]
    s1 -->|"revoke_session (backend/app/services/session_service.py)(db, current_session, response)"| s2
    s2 -->|"utc_now(data not statically known)"| s3
    s3 -. "datetime.now(UTC)" .-> s4
    s2 -->|"commit_or_flush(db)"| s5
    s5 -->|"current_command(db)"| s6
    s6 -. "getattr(db, 'info', None)" .-> s7
    s6 -. "isinstance(info, dict)" .-> s8
    s6 -. "info.get('command')" .-> s9
    s5 -. "db.flush(data not statically known)" .-> s10
    s5 -. "db.commit(data not statically known)" .-> s11
    s2 -->|"_cookie_options(data not statically known)"| s12
    click s1 "../modules/routers_session.md"
    click s2 "../modules/session_service.md"
    click s3 "../modules/time.md"
    click s5 "../modules/commands.md"
    click s6 "../modules/commands.md"
    click s12 "../modules/session_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `revoke_session (backend/app/routers/session.py)` | `response: Response`, `current_session: Annotated[UserSession, Depends(session_service.get_current_session)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | - | - | `MessageResponse(...)` |
| `revoke_session (backend/app/services/session_service.py)` | `db: AsyncSession`, `session: UserSession`, `response: Response` | - | `session.revoked_at` | - |
| `utc_now` | - | `UTC` | - | `datetime.now(...)` |
| `datetime.now` | - | - | - | - |
| `commit_or_flush` | `db` | - | - | - |
| `current_command` | `db` | - | - | `...` |
| `getattr` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `info.get` | - | - | - | - |
| `db.flush` | - | - | - | - |
| `db.commit` | - | - | - | - |
| `_cookie_options` | - | - | - | `{...}` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| revoke_session (backend/app/routers/session.py) | revoke_session (backend/app/services/session_service.py) | 43 | `session_service.revoke_session(db, current_session, response)` |
| revoke_session (backend/app/services/session_service.py) | utc_now | 217 | `utc_now(data not statically known)` |
| utc_now | datetime.now | 13 | `datetime.now(UTC)` |
| revoke_session (backend/app/services/session_service.py) | commit_or_flush | 218 | `commit_or_flush(db)` |
| commit_or_flush | current_command | 45 | `current_command(db)` |
| current_command | getattr | 39 | `getattr(db, 'info', None)` |
| current_command | isinstance | 40 | `isinstance(info, dict)` |
| current_command | info.get | 40 | `info.get('command')` |
| commit_or_flush | db.flush | 46 | `db.flush(data not statically known)` |
| commit_or_flush | db.commit | 48 | `db.commit(data not statically known)` |
| revoke_session (backend/app/services/session_service.py) | _cookie_options | 219 | `_cookie_options(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `utc_now` | `datetime.now` | 13 |
| external_call | `current_command` | `getattr` | 39 |
| external_call | `current_command` | `isinstance` | 40 |
| unresolved_call | `current_command` | `info.get` | 40 |
| unresolved_call | `commit_or_flush` | `db.flush` | 46 |
| unresolved_call | `commit_or_flush` | `db.commit` | 48 |
| step_limit | `revoke_session` | `first 12 steps` | 0 |

## Behavior

This flow starts at `revoke_session` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
