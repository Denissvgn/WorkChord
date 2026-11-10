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

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as revoke_session (backend/app/routers/session.py)
    participant p1 as revoke_session (backend/app/services/session_service.py)
    participant p2 as MessageResponse
    participant p3 as utc_now
    participant p4 as commit_or_flush
    participant p5 as _cookie_options
    participant p6 as response.delete_cookie
    participant p7 as datetime.now
    participant p8 as current_command
    participant p9 as get_settings
    participant p10 as db.flush
    participant p11 as db.commit
    participant p12 as getattr
    participant p13 as Settings
    participant p14 as isinstance
    participant p15 as info.get
    p0->>p1: revoke_session (backend/app/services/session_service.py)
    p0->>p2: MessageResponse
    p1->>p3: utc_now
    p1->>p4: commit_or_flush
    p1->>p5: _cookie_options
    p1-->>p6: response.delete_cookie(key=options[...], path=options[...], secure=options[...], httponly=True, samesite='lax')
    p3-->>p7: datetime.now(UTC)
    p4->>p8: current_command
    p5->>p9: get_settings
    p4-->>p10: db.flush
    p4-->>p11: db.commit
    p8-->>p12: getattr(db, 'info', None)
    p9->>p13: Settings
    p8-->>p14: isinstance(info, dict)
    p8-->>p15: info.get('command')
```

> Call sequence diagram shows 15 of 15 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 3 of 3 (0 omitted); unresolved 4 of 4 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 9; effect analysis evaluated: 7, partial: 0, unavailable: 2. Counts include steps omitted from the displayed trace.

Collector observations for 7 source steps with known totals: observed: 15, emitted: 15, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `revoke_session (backend/app/routers/session.py)` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `revoke_session (backend/app/services/session_service.py)` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `utc_now` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `datetime.now` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `commit_or_flush` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `current_command` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `getattr` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `db.flush` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `db.commit` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_cookie_options` | `available` | `evaluated` | `available` | `1` | `1` | `0` |

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
| commit_or_flush | current_command | 79 | `current_command(db)` |
| current_command | getattr | 73 | `getattr(db, 'info', None)` |
| current_command | isinstance | 74 | `isinstance(info, dict)` |
| current_command | info.get | 74 | `info.get('command')` |
| commit_or_flush | db.flush | 80 | `db.flush(data not statically known)` |
| commit_or_flush | db.commit | 82 | `db.commit(data not statically known)` |
| revoke_session (backend/app/services/session_service.py) | _cookie_options | 219 | `_cookie_options(data not statically known)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `utc_now` | `datetime.now` | 13 |
| external_call | `current_command` | `getattr` | 73 |
| external_call | `current_command` | `isinstance` | 74 |
| unresolved_call | `current_command` | `info.get` | 74 |
| unresolved_call | `commit_or_flush` | `db.flush` | 80 |
| unresolved_call | `commit_or_flush` | `db.commit` | 82 |
| step_limit | `revoke_session` | `first 12 steps` | 0 |

## Behavior

This flow starts at `revoke_session` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
