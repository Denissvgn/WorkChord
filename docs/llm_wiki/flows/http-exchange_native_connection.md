# exchange_native_connection

**Entry point:** `exchange_native_connection` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [config](../modules/config.md), [native_session_service](../modules/native_session_service.md), [routers_identity](../modules/routers_identity.md), [session_service](../modules/session_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as exchange_native_connection
    participant p1 as NativeSessionService(…).exchange
    participant p2 as NativeSessionService
    participant p3 as get_client_ip
    participant p4 as ip_address
    participant p5 as any
    participant p6 as ip_network
    participant p7 as get_settings
    participant p8 as Settings
    participant p9 as request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)
    participant p10 as forwarded_for.split(…)[…].strip
    participant p11 as forwarded_for.split
    participant p12 as real_ip.strip
    participant p13 as request.headers.get (backend/app/routers/ident…exchange_native_connection)
    p0-->>p1: NativeSessionService(…).exchange
    p0->>p2: NativeSessionService
    p0->>p3: get_client_ip
    p3-->>p4: ip_address
    p3-->>p5: any
    p3-->>p6: ip_network
    p3->>p7: get_settings
    p7->>p8: Settings
    p3-->>p9: request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)
    p3-->>p10: forwarded_for.split(…)[…].strip
    p3-->>p11: forwarded_for.split
    p3-->>p9: request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)
    p3-->>p12: real_ip.strip
    p0-->>p13: request.headers.get (backend/app/routers/ident…exchange_native_connection)
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. exchange_native_connection"]
    s2["2. NativeSessionService(…).exchange"]
    s3["3. NativeSessionService"]
    s4["4. get_client_ip"]
    s5["5. ip_address"]
    s6["6. any"]
    s7["7. ip_network"]
    s8["8. get_settings"]
    s9["9. Settings"]
    s10["10. request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)"]
    s11["11. forwarded_for.split(…)[…].strip"]
    s12["12. forwarded_for.split"]
    s1 -. "NativeSessionService(…).exchange(data.request_id, data.code_verifier, ..., request.headers.get(...))" .-> s2
    s1 -->|"NativeSessionService(db)"| s3
    s1 -->|"get_client_ip(request)"| s4
    s4 -. "ip_address(direct_ip)" .-> s5
    s4 -. "any(...)" .-> s6
    s4 -. "ip_network(network, strict=False)" .-> s7
    s4 -->|"get_settings(data not statically known)"| s8
    s8 -->|"Settings(data not statically known)"| s9
    s4 -. "request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)('X-Forwarded-For')" .-> s10
    s4 -. "forwarded_for.split(…)[…].strip(data not statically known)" .-> s11
    s4 -. "forwarded_for.split(',')" .-> s12
    click s1 "../modules/routers_identity.md"
    click s3 "../modules/native_session_service.md"
    click s4 "../modules/session_service.md"
    click s8 "../modules/config.md"
    click s9 "../modules/config.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `exchange_native_connection` | `data: NativeConnectionExchange`, `request: Request`, `response: Response`, `db: Database` | - | `response.headers[...]` | `...` |
| `NativeSessionService(…).exchange` | - | - | - | - |
| `NativeSessionService` | - | - | - | - |
| `get_client_ip` | `request: Request` | - | - | `...`, `real_ip.strip(...)`, `direct_ip` |
| `ip_address` | - | - | - | - |
| `any` | - | - | - | - |
| `ip_network` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)` | - | - | - | - |
| `forwarded_for.split(…)[…].strip` | - | - | - | - |
| `forwarded_for.split` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| exchange_native_connection | NativeSessionService(…).exchange | 86 | `NativeSessionService(db).exchange(data.request_id, data.code_verifier, ..., request.headers.get(...))` |
| exchange_native_connection | NativeSessionService | 86 | `NativeSessionService(db)` |
| exchange_native_connection | get_client_ip | 87 | `get_client_ip(request)` |
| get_client_ip | ip_address | 52 | `ip_address(direct_ip)` |
| get_client_ip | any | 53 | `any(...)` |
| get_client_ip | ip_network | 54 | `ip_network(network, strict=False)` |
| get_client_ip | get_settings | 55 | `get_settings(data not statically known)` |
| get_settings | Settings | 480 | `Settings(data not statically known)` |
| get_client_ip | request.headers.get (backend/app/services/sess…n_service.py:get_client_ip) | 60 | `request.headers.get('X-Forwarded-For')` |
| get_client_ip | forwarded_for.split(…)[…].strip | 62 | `forwarded_for.split(',')[0].strip(data not statically known)` |
| get_client_ip | forwarded_for.split | 62 | `forwarded_for.split(',')` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `exchange_native_connection` | `NativeSessionService(db).exchange` | 86 |
| external_call | `get_client_ip` | `ip_address` | 52 |
| external_call | `get_client_ip` | `any` | 53 |
| external_call | `get_client_ip` | `ip_network` | 54 |
| unresolved_call | `get_client_ip` | `request.headers.get` | 60 |
| unresolved_call | `get_client_ip` | `forwarded_for.split(',')[0].strip` | 62 |
| unresolved_call | `get_client_ip` | `forwarded_for.split` | 62 |
| step_limit | `exchange_native_connection` | `first 12 steps` | 0 |

## Behavior

Checks the device verifier against the S256 challenge before revealing connection state. Pending consent produces a pending response. Approved exchange locks principal then session, rechecks enabled human identity and valid browser approval, and conditionally consumes the request in the same transaction as native session issuance. Replay or expiry fails explicitly.
