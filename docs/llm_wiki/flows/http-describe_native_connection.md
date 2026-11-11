# describe_native_connection

**Entry point:** `describe_native_connection` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [authority](../modules/authority.md), [identity_service](../modules/identity_service.md), [native_session_service](../modules/native_session_service.md), [routers_identity](../modules/routers_identity.md), and 1 more

**Complete modules touched:**

- [authority](../modules/authority.md)
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
    participant p3 as NativeSessionService.human
    participant p4 as internal_authority
    participant p5 as NativeSessionService.connection
    participant p6 as self.db.info.get
    participant p7 as db.info.get
    participant p8 as self.db.get
    participant p9 as AuthorityError
    participant p10 as digest
    participant p11 as as_utc
    participant p12 as utc_now
    participant p13 as hashlib.sha256(…).hexdigest
    participant p14 as value.replace
    participant p15 as datetime.now
    participant p16 as hashlib.sha256
    participant p17 as value.astimezone
    participant p18 as value.encode
    p0->>p1: NativeSessionService.describe
    p0->>p2: NativeSessionService
    p1->>p3: NativeSessionService.human
    p1->>p4: internal_authority
    p1->>p5: NativeSessionService.connection
    p3-->>p6: self.db.info.get('authority')
    p4-->>p7: db.info.get('authority_internal', False)
    p5-->>p8: self.db.get(NativeConnection, digest(...))
    p3->>p9: AuthorityError
    p5->>p10: digest
    p5->>p9: AuthorityError
    p5->>p11: as_utc
    p5->>p12: utc_now
    p5->>p9: AuthorityError
    p10-->>p13: hashlib.sha256(…).hexdigest
    p11-->>p14: value.replace(tzinfo=UTC)
    p12-->>p15: datetime.now(UTC)
    p10-->>p16: hashlib.sha256(value.encode(...))
    p11-->>p17: value.astimezone(UTC)
    p10-->>p18: value.encode
```

> Call sequence diagram shows 20 of 20 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 2 of 2 (0 omitted); unresolved 7 of 7 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 12; effect analysis evaluated: 8, partial: 0, unavailable: 4. Counts include steps omitted from the displayed trace.

Collector observations for 8 source steps with known totals: observed: 24, emitted: 24, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `describe_native_connection` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `NativeSessionService.describe` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `NativeSessionService.human` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `self.db.info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AuthorityError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `internal_authority` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `db.info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `NativeSessionService.connection` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `self.db.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `digest` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `hashlib.sha256(…).hexdigest` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `hashlib.sha256` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. describe_native_connection"]
    s2["2. NativeSessionService.describe"]
    s3["3. NativeSessionService.human"]
    s4["4. self.db.info.get"]
    s5["5. AuthorityError"]
    s6["6. internal_authority"]
    s7["7. db.info.get"]
    s8["8. NativeSessionService.connection"]
    s9["9. self.db.get"]
    s10["10. digest"]
    s11["11. hashlib.sha256(…).hexdigest"]
    s12["12. hashlib.sha256"]
    s1 -->|"NativeSessionService.describe(request_id)"| s2
    s2 -->|"NativeSessionService.human(data not statically known)"| s3
    s3 -. "self.db.info.get('authority')" .-> s4
    s3 -->|"AuthorityError('human_session_required', 'Sign in with a human account to connect a device.', 403)"| s5
    s2 -->|"internal_authority(self.db)"| s6
    s6 -. "db.info.get('authority_internal', False)" .-> s7
    s2 -->|"NativeSessionService.connection(request_id)"| s8
    s8 -. "self.db.get(NativeConnection, digest(...))" .-> s9
    s8 -->|"digest(request_id)"| s10
    s10 -. "hashlib.sha256(…).hexdigest(data not statically known)" .-> s11
    s10 -. "hashlib.sha256(value.encode(...))" .-> s12
    click s1 "../modules/routers_identity.md"
    click s2 "../modules/native_session_service.md"
    click s3 "../modules/native_session_service.md"
    click s5 "../modules/authority.md"
    click s6 "../modules/authority.md"
    click s8 "../modules/native_session_service.md"
    click s10 "../modules/identity_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `describe_native_connection` | `request_id: str`, `response: Response`, `db: Database` | - | `response.headers[...]` | `...` |
| `NativeSessionService.describe` | `request_id` | `self.db` | - | `{...}` |
| `NativeSessionService.human` | - | - | - | `authority` |
| `self.db.info.get` | - | - | - | - |
| `AuthorityError` | - | - | - | - |
| `internal_authority` | `db` | - | `db.info[...]`, `db.info[...]` | - |
| `db.info.get` | - | - | - | - |
| `NativeSessionService.connection` | `request_id` | `NativeConnection` | - | `row` |
| `self.db.get` | - | - | - | - |
| `digest` | `value: str` | - | - | `...` |
| `hashlib.sha256(…).hexdigest` | - | - | - | - |
| `hashlib.sha256` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| describe_native_connection | NativeSessionService.describe | 98 | `NativeSessionService(db).describe(request_id)` |
| NativeSessionService.describe | NativeSessionService.human | 64 | `self.human(data not statically known)` |
| NativeSessionService.human | self.db.info.get | 26 | `self.db.info.get('authority')` |
| NativeSessionService.human | AuthorityError | 28 | `AuthorityError('human_session_required', 'Sign in with a human account to connect a device.', 403)` |
| NativeSessionService.describe | internal_authority | 65 | `internal_authority(self.db)` |
| internal_authority | db.info.get | 87 | `db.info.get('authority_internal', False)` |
| NativeSessionService.describe | NativeSessionService.connection | 66 | `self.connection(request_id)` |
| NativeSessionService.connection | self.db.get | 32 | `self.db.get(NativeConnection, digest(...))` |
| NativeSessionService.connection | digest | 32 | `digest(request_id)` |
| digest | hashlib.sha256(…).hexdigest | 27 | `hashlib.sha256(value.encode()).hexdigest(data not statically known)` |
| digest | hashlib.sha256 | 27 | `hashlib.sha256(value.encode(...))` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `NativeSessionService.human` | `self.db.info.get` | 26 |
| unresolved_call | `internal_authority` | `db.info.get` | 87 |
| unresolved_call | `NativeSessionService.connection` | `self.db.get` | 32 |
| unresolved_call | `digest` | `hashlib.sha256(value.encode()).hexdigest` | 27 |
| external_call | `digest` | `hashlib.sha256` | 27 |
| step_limit | `describe_native_connection` | `first 12 steps` | 0 |

## Behavior

Requires a human session and returns only the display code, expiry, and approval state for a live connection. It does not return the challenge, approving session identity, or token.
