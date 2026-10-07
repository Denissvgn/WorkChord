# transfer_guest

**Entry point:** `transfer_guest` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [config](../modules/config.md), [identity_service](../modules/identity_service.md), [routers_identity](../modules/routers_identity.md), [session_service](../modules/session_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as transfer_guest
    participant p1 as IdentityService(…).transfer_guest
    participant p2 as IdentityService
    participant p3 as request.cookies.get
    participant p4 as response.delete_cookie
    participant p5 as _cookie_options
    participant p6 as get_settings
    participant p7 as Settings
    p0-->>p1: IdentityService(…).transfer_guest
    p0->>p2: IdentityService
    p0-->>p3: request.cookies.get
    p0-->>p4: response.delete_cookie
    p0->>p5: _cookie_options
    p5->>p6: get_settings
    p6->>p7: Settings
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. transfer_guest"]
    s2["2. IdentityService(…).transfer_guest"]
    s3["3. IdentityService"]
    s4["4. request.cookies.get"]
    s5["5. response.delete_cookie"]
    s6["6. _cookie_options"]
    s7["7. get_settings"]
    s8["8. Settings"]
    s1 -. "IdentityService(…).transfer_guest(..., ..., operator_reason=data.reason, guest_id=data.guest_session_id)" .-> s2
    s1 -->|"IdentityService(db)"| s3
    s1 -. "request.cookies.get('workchord_guest_transfer')" .-> s4
    s1 -. "response.delete_cookie('workchord_guest_transfer', path=...)" .-> s5
    s1 -->|"_cookie_options(data not statically known)"| s6
    s6 -->|"get_settings(data not statically known)"| s7
    s7 -->|"Settings(data not statically known)"| s8
    click s1 "../modules/routers_identity.md"
    click s3 "../modules/identity_service.md"
    click s6 "../modules/session_service.md"
    click s7 "../modules/config.md"
    click s8 "../modules/config.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `transfer_guest` | `data: GuestTransferRequest`, `request: Request`, `response: Response`, `db: Database` | - | - | `result` |
| `IdentityService(…).transfer_guest` | - | - | - | - |
| `IdentityService` | - | - | - | - |
| `request.cookies.get` | - | - | - | - |
| `response.delete_cookie` | - | - | - | - |
| `_cookie_options` | - | - | - | `{...}` |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| transfer_guest | IdentityService(…).transfer_guest | 286 | `IdentityService(db).transfer_guest(..., ..., operator_reason=data.reason, guest_id=data.guest_session_id)` |
| transfer_guest | IdentityService | 286 | `IdentityService(db)` |
| transfer_guest | request.cookies.get | 286 | `request.cookies.get('workchord_guest_transfer')` |
| transfer_guest | response.delete_cookie | 288 | `response.delete_cookie('workchord_guest_transfer', path=...)` |
| transfer_guest | _cookie_options | 288 | `_cookie_options(data not statically known)` |
| _cookie_options | get_settings | 37 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `transfer_guest` | `IdentityService(db).transfer_guest` | 286 |
| unresolved_call | `transfer_guest` | `request.cookies.get` | 286 |
| unresolved_call | `transfer_guest` | `response.delete_cookie` | 288 |

## Behavior

This flow starts at `transfer_guest` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

Transfers supported guest-owned personal data only with current guest-token proof or reasoned operator recovery. Attribution stays on its original anonymous session; public links rotate and the guest token is revoked.
