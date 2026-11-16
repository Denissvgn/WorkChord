# describe_native_connection

**Entry point:** `describe_native_connection` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [authority](../modules/authority.md), [config](../modules/config.md), [identity_service](../modules/identity_service.md), [native_session_service](../modules/native_session_service.md), and 2 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [identity_service](../modules/identity_service.md)
- [native_session_service](../modules/native_session_service.md)
- [routers_identity](../modules/routers_identity.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as describe_native_connection
    participant p1 as NativeSessionService.describe
    participant p2 as NativeSessionService
    participant p3 as NativeSessionService.approver
    participant p4 as internal_authority
    participant p5 as NativeSessionService.connection
    participant p6 as self.db.info.get
    participant p7 as db.info.get
    participant p8 as self.db.get
    participant p9 as get_settings
    participant p10 as digest
    participant p11 as AuthorityError
    participant p12 as as_utc
    participant p13 as utc_now
    participant p14 as Settings
    participant p15 as hashlib.sha256(…).hexdigest
    participant p16 as value.replace
    participant p17 as datetime.now
    participant p18 as hashlib.sha256
    participant p19 as value.astimezone
    participant p20 as value.encode
    p0->>p1: NativeSessionService.describe
    p0->>p2: NativeSessionService
    p1->>p3: NativeSessionService.approver
    p1->>p4: internal_authority
    p1->>p5: NativeSessionService.connection
    p1->>p3: NativeSessionService.approver
    p3-->>p6: self.db.info.get('authority')
    p4-->>p7: db.info.get('authority_internal', False)
    p5-->>p8: self.db.get(NativeConnection, digest(...))
    p3->>p9: get_settings
    p5->>p10: digest
    p3->>p11: AuthorityError
    p5->>p11: AuthorityError
    p3->>p11: AuthorityError
    p5->>p12: as_utc
    p3->>p11: AuthorityError
    p5->>p13: utc_now
    p5->>p11: AuthorityError
    p9->>p14: Settings
    p10-->>p15: hashlib.sha256(…).hexdigest
    p12-->>p16: value.replace(tzinfo=UTC)
    p13-->>p17: datetime.now(UTC)
    p10-->>p18: hashlib.sha256(value.encode(...))
    p12-->>p19: value.astimezone(UTC)
    p10-->>p20: value.encode
```

> Call sequence diagram shows 25 of 25 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 2 of 2 (0 omitted); unresolved 7 of 7 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 17; effect analysis evaluated: 10, partial: 0, unavailable: 7. Counts include steps omitted from the displayed trace.

Collector observations for 10 source steps with known totals: observed: 30, emitted: 30, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `describe_native_connection` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `NativeSessionService.describe` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `NativeSessionService.approver` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `self.db.info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `internal_authority` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `db.info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `NativeSessionService.connection` | `available` | `evaluated` | `available` | `3` | `3` | `0` |

```mermaid
flowchart LR
    s1["1. describe_native_connection"]
    s2["2. NativeSessionService.describe"]
    s3["3. NativeSessionService.approver"]
    s4["4. self.db.info.get"]
    s5["5. get_settings"]
    s6["6. Settings"]
    s7["7. AuthorityError"]
    s8["8. AuthorityError"]
    s9["9. AuthorityError"]
    s10["10. internal_authority"]
    s11["11. db.info.get"]
    s12["12. NativeSessionService.connection"]
    s1 -->|"NativeSessionService.describe(request_id)"| s2
    s2 -->|"NativeSessionService.approver(data not statically known)"| s3
    s3 -. "self.db.info.get('authority')" .-> s4
    s3 -->|"get_settings(data not statically known)"| s5
    s5 -->|"Settings(data not statically known)"| s6
    s3 -->|"AuthorityError('browser_session_required', 'Reload this page, then approve the connection.', 403)"| s7
    s3 -->|"AuthorityError('human_session_required', 'Sign in with a human account to connect a device.', 403)"| s8
    s3 -->|"AuthorityError('human_session_required', 'Sign in with a human account to connect a device.', 403)"| s9
    s2 -->|"internal_authority(self.db)"| s10
    s10 -. "db.info.get('authority_internal', False)" .-> s11
    s2 -->|"NativeSessionService.connection(request_id)"| s12
    click s1 "../modules/routers_identity.md"
    click s2 "../modules/native_session_service.md"
    click s3 "../modules/native_session_service.md"
    click s5 "../modules/config.md"
    click s6 "../modules/config.md"
    click s7 "../modules/authority.md"
    click s8 "../modules/authority.md"
    click s9 "../modules/authority.md"
    click s10 "../modules/authority.md"
    click s12 "../modules/native_session_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `describe_native_connection` | `request_id: str`, `response: Response`, `db: Database` | - | `response.headers[...]` | `...` |
| `NativeSessionService.describe` | `request_id` | `self.db` | - | `{...}` |
| `NativeSessionService.approver` | `row` | - | - | `authority`, `authority` |
| `self.db.info.get` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `internal_authority` | `db` | - | `db.info[...]`, `db.info[...]` | - |
| `db.info.get` | - | - | - | - |
| `NativeSessionService.connection` | `request_id` | `NativeConnection` | - | `row` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| describe_native_connection | NativeSessionService.describe | 118 | `NativeSessionService(db).describe(request_id)` |
| NativeSessionService.describe | NativeSessionService.approver | 81 | `self.approver(data not statically known)` |
| NativeSessionService.approver | self.db.info.get | 33 | `self.db.info.get('authority')` |
| NativeSessionService.approver | get_settings | 35 | `get_settings(data not statically known)` |
| get_settings | Settings | 524 | `Settings(data not statically known)` |
| NativeSessionService.approver | AuthorityError | 37 | `AuthorityError('browser_session_required', 'Reload this page, then approve the connection.', 403)` |
| NativeSessionService.approver | AuthorityError | 39 | `AuthorityError('human_session_required', 'Sign in with a human account to connect a device.', 403)` |
| NativeSessionService.approver | AuthorityError | 44 | `AuthorityError('human_session_required', 'Sign in with a human account to connect a device.', 403)` |
| NativeSessionService.describe | internal_authority | 82 | `internal_authority(self.db)` |
| internal_authority | db.info.get | 92 | `db.info.get('authority_internal', False)` |
| NativeSessionService.describe | NativeSessionService.connection | 83 | `self.connection(request_id)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `NativeSessionService.approver` | `self.db.info.get` | 33 |
| unresolved_call | `internal_authority` | `db.info.get` | 92 |
| step_limit | `describe_native_connection` | `first 12 steps` | 0 |

## Behavior

Requires a human session and returns only the display code, expiry, and approval state for a live connection. It does not return the challenge, approving session identity, or token.
