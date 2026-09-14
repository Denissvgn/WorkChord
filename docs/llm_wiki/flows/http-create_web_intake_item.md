# create_web_intake_item

**Entry point:** `create_web_intake_item` (`http`)
**Source:** [routers_intake](../modules/routers_intake.md)
**Modules touched:** [config](../modules/config.md), [routers_intake](../modules/routers_intake.md), [session_service](../modules/session_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_web_intake_item
    participant p1 as WebIntakeRequest.model_validate
    participant p2 as get_client_ip
    participant p3 as ip_address
    participant p4 as any
    participant p5 as ip_network
    participant p6 as get_settings
    participant p7 as Settings
    participant p8 as request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)
    participant p9 as forwarded_for.split(…)[…].strip
    participant p10 as forwarded_for.split
    participant p11 as real_ip.strip
    participant p12 as service.create_triage_item
    participant p13 as request.headers.get (backend/app/routers/intake.py:create_web_intake_item)
    participant p14 as HTTPException
    participant p15 as str
    p0-->>p1: WebIntakeRequest.model_validate
    p0->>p2: get_client_ip
    p2-->>p3: ip_address
    p2-->>p4: any
    p2-->>p5: ip_network
    p2->>p6: get_settings
    p6->>p7: Settings
    p2-->>p8: request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)
    p2-->>p9: forwarded_for.split(…)[…].strip
    p2-->>p10: forwarded_for.split
    p2-->>p8: request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)
    p2-->>p11: real_ip.strip
    p0-->>p12: service.create_triage_item
    p0-->>p13: request.headers.get (backend/app/routers/intake.py:create_web_intake_item)
    p0-->>p14: HTTPException
    p0-->>p15: str
    p0-->>p14: HTTPException
    p0-->>p15: str
    p0-->>p14: HTTPException
    p0-->>p15: str
    p0-->>p14: HTTPException
    p0-->>p15: str
    p0-->>p15: str
    p0-->>p14: HTTPException
    p0-->>p15: str
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. create_web_intake_item"]
    s2["2. WebIntakeRequest.model_validate"]
    s3["3. get_client_ip"]
    s4["4. ip_address"]
    s5["5. any"]
    s6["6. ip_network"]
    s7["7. get_settings"]
    s8["8. Settings"]
    s9["9. request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)"]
    s10["10. forwarded_for.split(…)[…].strip"]
    s11["11. forwarded_for.split"]
    s12["12. request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)"]
    s1 -. "WebIntakeRequest.model_validate(raw_data)" .-> s2
    s1 -->|"get_client_ip(request)"| s3
    s3 -. "ip_address(direct_ip)" .-> s4
    s3 -. "any(...)" .-> s5
    s3 -. "ip_network(network, strict=False)" .-> s6
    s3 -->|"get_settings(data not statically known)"| s7
    s7 -->|"Settings(data not statically known)"| s8
    s3 -. "request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)('X-Forwarded-For')" .-> s9
    s3 -. "forwarded_for.split(…)[…].strip(data not statically known)" .-> s10
    s3 -. "forwarded_for.split(',')" .-> s11
    s3 -. "request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)('X-Real-IP')" .-> s12
    click s1 "../modules/routers_intake.md"
    click s3 "../modules/session_service.md"
    click s7 "../modules/config.md"
    click s8 "../modules/config.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_web_intake_item` | `request: Request`, `raw_data: Annotated[Any, Body(...)]`, `service: Annotated[WebIntakeService, Depends(get_web_intake_service)]`, `authorization: Annotated[Optional[str], Header(alias='Authorization')]` | `ValidationError`, `status`, `WebIntakeConfigurationError`, `status`, `WebIntakeUnauthorizedError`, `status`, `WebIntakeRateLimitError`, `status` | - | `...` |
| `WebIntakeRequest.model_validate` | - | - | - | - |
| `get_client_ip` | `request: Request` | - | - | `...`, `real_ip.strip(...)`, `direct_ip` |
| `ip_address` | - | - | - | - |
| `any` | - | - | - | - |
| `ip_network` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)` | - | - | - | - |
| `forwarded_for.split(…)[…].strip` | - | - | - | - |
| `forwarded_for.split` | - | - | - | - |
| `request.headers.get (backend/app/services/sess…n_service.py:get_client_ip)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_web_intake_item | WebIntakeRequest.model_validate | 48 | `WebIntakeRequest.model_validate(raw_data)` |
| create_web_intake_item | get_client_ip | 49 | `get_client_ip(request)` |
| get_client_ip | ip_address | 50 | `ip_address(direct_ip)` |
| get_client_ip | any | 51 | `any(...)` |
| get_client_ip | ip_network | 52 | `ip_network(network, strict=False)` |
| get_client_ip | get_settings | 53 | `get_settings(data not statically known)` |
| get_settings | Settings | 469 | `Settings(data not statically known)` |
| get_client_ip | request.headers.get (backend/app/services/sess…n_service.py:get_client_ip) | 58 | `request.headers.get('X-Forwarded-For')` |
| get_client_ip | forwarded_for.split(…)[…].strip | 60 | `forwarded_for.split(',')[0].strip(data not statically known)` |
| get_client_ip | forwarded_for.split | 60 | `forwarded_for.split(',')` |
| get_client_ip | request.headers.get (backend/app/services/sess…n_service.py:get_client_ip) | 61 | `request.headers.get('X-Real-IP')` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `create_web_intake_item` | `WebIntakeRequest.model_validate` | 48 |
| external_call | `get_client_ip` | `ip_address` | 50 |
| external_call | `get_client_ip` | `any` | 51 |
| external_call | `get_client_ip` | `ip_network` | 52 |
| unresolved_call | `get_client_ip` | `request.headers.get` | 58 |
| unresolved_call | `get_client_ip` | `forwarded_for.split(',')[0].strip` | 60 |
| unresolved_call | `get_client_ip` | `forwarded_for.split` | 60 |
| unresolved_call | `get_client_ip` | `request.headers.get` | 61 |
| step_limit | `create_web_intake_item` | `first 12 steps` | 0 |

## Behavior

This flow starts at `create_web_intake_item` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
