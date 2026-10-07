# start_native_connection

**Entry point:** `start_native_connection` (`http`)
**Source:** [routers_identity](../modules/routers_identity.md)
**Modules touched:** [config](../modules/config.md), [native_session_service](../modules/native_session_service.md), [routers_identity](../modules/routers_identity.md), [session_service](../modules/session_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as start_native_connection
    participant p1 as NativeSessionService(…).start
    participant p2 as NativeSessionService
    participant p3 as get_client_ip
    participant p4 as ip_address
    participant p5 as any
    participant p6 as ip_network
    participant p7 as get_settings
    participant p8 as Settings
    participant p9 as request.headers.get
    participant p10 as forwarded_for.split(…)[…].strip
    participant p11 as forwarded_for.split
    participant p12 as real_ip.strip
    p0-->>p1: NativeSessionService(…).start
    p0->>p2: NativeSessionService
    p0->>p3: get_client_ip
    p3-->>p4: ip_address
    p3-->>p5: any
    p3-->>p6: ip_network
    p3->>p7: get_settings
    p7->>p8: Settings
    p3-->>p9: request.headers.get
    p3-->>p10: forwarded_for.split(…)[…].strip
    p3-->>p11: forwarded_for.split
    p3-->>p9: request.headers.get
    p3-->>p12: real_ip.strip
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. start_native_connection"]
    s2["2. NativeSessionService(…).start"]
    s3["3. NativeSessionService"]
    s4["4. get_client_ip"]
    s5["5. ip_address"]
    s6["6. any"]
    s7["7. ip_network"]
    s8["8. get_settings"]
    s9["9. Settings"]
    s10["10. request.headers.get"]
    s11["11. forwarded_for.split(…)[…].strip"]
    s12["12. forwarded_for.split"]
    s1 -. "NativeSessionService(…).start(data.code_challenge, ...)" .-> s2
    s1 -->|"NativeSessionService(db)"| s3
    s1 -->|"get_client_ip(request)"| s4
    s4 -. "ip_address(direct_ip)" .-> s5
    s4 -. "any(...)" .-> s6
    s4 -. "ip_network(network, strict=False)" .-> s7
    s4 -->|"get_settings(data not statically known)"| s8
    s8 -->|"Settings(data not statically known)"| s9
    s4 -. "request.headers.get('X-Forwarded-For')" .-> s10
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
| `start_native_connection` | `data: NativeConnectionStart`, `request: Request`, `response: Response`, `db: Database` | - | `response.headers[...]` | `...` |
| `NativeSessionService(…).start` | - | - | - | - |
| `NativeSessionService` | - | - | - | - |
| `get_client_ip` | `request: Request` | - | - | `...`, `real_ip.strip(...)`, `direct_ip` |
| `ip_address` | - | - | - | - |
| `any` | - | - | - | - |
| `ip_network` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `request.headers.get` | - | - | - | - |
| `forwarded_for.split(…)[…].strip` | - | - | - | - |
| `forwarded_for.split` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| start_native_connection | NativeSessionService(…).start | 79 | `NativeSessionService(db).start(data.code_challenge, ...)` |
| start_native_connection | NativeSessionService | 79 | `NativeSessionService(db)` |
| start_native_connection | get_client_ip | 79 | `get_client_ip(request)` |
| get_client_ip | ip_address | 52 | `ip_address(direct_ip)` |
| get_client_ip | any | 53 | `any(...)` |
| get_client_ip | ip_network | 54 | `ip_network(network, strict=False)` |
| get_client_ip | get_settings | 55 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| get_client_ip | request.headers.get | 60 | `request.headers.get('X-Forwarded-For')` |
| get_client_ip | forwarded_for.split(…)[…].strip | 62 | `forwarded_for.split(',')[0].strip(data not statically known)` |
| get_client_ip | forwarded_for.split | 62 | `forwarded_for.split(',')` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `start_native_connection` | `NativeSessionService(db).start` | 79 |
| external_call | `get_client_ip` | `ip_address` | 52 |
| external_call | `get_client_ip` | `any` | 53 |
| external_call | `get_client_ip` | `ip_network` | 54 |
| unresolved_call | `get_client_ip` | `request.headers.get` | 60 |
| unresolved_call | `get_client_ip` | `forwarded_for.split(',')[0].strip` | 62 |
| unresolved_call | `get_client_ip` | `forwarded_for.split` | 62 |
| step_limit | `start_native_connection` | `first 12 steps` | 0 |

## Behavior

Creates a ten-minute request with a hashed random identity, an S256 challenge, and a displayed verification code. It uses managed authentication, bounded attempt counts and bounded expired-request cleanup. The response points to a local browser consent path and carries no access token or device verifier.
