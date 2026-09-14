# discover_agent_skill_bundles

**Entry point:** `discover_agent_skill_bundles` (`http`)
**Source:** [agent_skill_bundles](../modules/agent_skill_bundles.md)
**Modules touched:** [agent_skill_bundles](../modules/agent_skill_bundles.md), [config](../modules/config.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as discover_agent_skill_bundles
    participant p1 as get_settings().api_prefix.rstrip
    participant p2 as get_settings
    participant p3 as Settings
    participant p4 as _resolve_payload
    participant p5 as action
    participant p6 as HTTPException
    participant p7 as service.discovery_payload
    participant p8 as _response
    participant p9 as cache_control.replace
    participant p10 as _etag_matches
    participant p11 as if_none_match.split
    participant p12 as candidate.strip
    participant p13 as value.removeprefix
    participant p14 as request.headers.get
    participant p15 as Response
    p0-->>p1: get_settings().api_prefix.rstrip
    p0->>p2: get_settings
    p2->>p3: Settings
    p0->>p4: _resolve_payload
    p4-->>p5: action
    p4-->>p6: HTTPException
    p4-->>p6: HTTPException
    p0-->>p7: service.discovery_payload
    p0->>p8: _response
    p8->>p2: get_settings
    p8-->>p9: cache_control.replace
    p8->>p10: _etag_matches
    p10-->>p11: if_none_match.split
    p10-->>p12: candidate.strip
    p10-->>p13: value.removeprefix
    p8-->>p14: request.headers.get
    p8-->>p15: Response
    p8-->>p15: Response
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. discover_agent_skill_bundles"]
    s2["2. get_settings().api_prefix.rstrip"]
    s3["3. get_settings"]
    s4["4. Settings"]
    s5["5. _resolve_payload"]
    s6["6. action"]
    s7["7. HTTPException"]
    s8["8. HTTPException"]
    s9["9. service.discovery_payload"]
    s10["10. _response"]
    s11["11. get_settings"]
    s12["12. cache_control.replace"]
    s1 -. "get_settings().api_prefix.rstrip('/')" .-> s2
    s1 -->|"get_settings(data not statically known)"| s3
    s3 -->|"Settings(data not statically known)"| s4
    s1 -->|"_resolve_payload(...)"| s5
    s5 -. "action(data not statically known)" .-> s6
    s5 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Skill bundle resource not found.')" .-> s7
    s5 -. "HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Skill bundle artifacts are unavailable.')" .-> s8
    s1 -. "service.discovery_payload(...)" .-> s9
    s1 -->|"_response(payload, request)"| s10
    s10 -->|"get_settings(data not statically known)"| s11
    s10 -. "cache_control.replace('public,', 'private,', 1)" .-> s12
    click s1 "../modules/agent_skill_bundles.md"
    click s3 "../modules/config.md"
    click s4 "../modules/config.md"
    click s5 "../modules/agent_skill_bundles.md"
    click s10 "../modules/agent_skill_bundles.md"
    click s11 "../modules/config.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `discover_agent_skill_bundles` | `request: Request`, `service: Annotated[AgentSkillBundleService, Depends(get_agent_skill_bundle_service)]`, `_access: Annotated[None, Depends(require_agent_skill_bundle_access)]` | - | - | `_response(...)` |
| `get_settings().api_prefix.rstrip` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `_resolve_payload` | `action: Callable[[], SkillBundlePayload]` | `SkillBundleNotFoundError`, `status`, `SkillBundleArtifactError`, `status` | - | `action(...)` |
| `action` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `service.discovery_payload` | - | - | - | - |
| `_response` | `payload: SkillBundlePayload`, `request: Request` | `status` | `headers[...]` | `Response(...)`, `Response(...)` |
| `get_settings` | - | - | - | `Settings(...)` |
| `cache_control.replace` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| discover_agent_skill_bundles | get_settings().api_prefix.rstrip | 117 | `get_settings().api_prefix.rstrip('/')` |
| discover_agent_skill_bundles | get_settings | 117 | `get_settings(data not statically known)` |
| get_settings | Settings | 469 | `Settings(data not statically known)` |
| discover_agent_skill_bundles | _resolve_payload | 118 | `_resolve_payload(...)` |
| _resolve_payload | action | 67 | `action(data not statically known)` |
| _resolve_payload | HTTPException | 69 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Skill bundle resource not found.')` |
| _resolve_payload | HTTPException | 74 | `HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Skill bundle artifacts are unavailable.')` |
| discover_agent_skill_bundles | service.discovery_payload | 119 | `service.discovery_payload(...)` |
| discover_agent_skill_bundles | _response | 121 | `_response(payload, request)` |
| _response | get_settings | 92 | `get_settings(data not statically known)` |
| _response | cache_control.replace | 93 | `cache_control.replace('public,', 'private,', 1)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `discover_agent_skill_bundles` | `get_settings().api_prefix.rstrip` | 117 |
| unresolved_call | `_resolve_payload` | `action` | 67 |
| external_call | `_resolve_payload` | `HTTPException` | 69 |
| external_call | `_resolve_payload` | `HTTPException` | 74 |
| unresolved_call | `discover_agent_skill_bundles` | `service.discovery_payload` | 119 |
| unresolved_call | `_response` | `cache_control.replace` | 93 |
| step_limit | `discover_agent_skill_bundles` | `first 12 steps` | 0 |

## Behavior

This flow starts at `discover_agent_skill_bundles` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
