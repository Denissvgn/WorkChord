# get_agent_skill_bundle_manifest

**Entry point:** `get_agent_skill_bundle_manifest` (`http`)
**Source:** [agent_skill_bundles](../modules/agent_skill_bundles.md)
**Modules touched:** [agent_skill_bundles](../modules/agent_skill_bundles.md), [config](../modules/config.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_agent_skill_bundle_manifest
    participant p1 as _resolve_payload
    participant p2 as action
    participant p3 as HTTPException
    participant p4 as service.manifest_payload
    participant p5 as _response
    participant p6 as get_settings
    participant p7 as Settings
    participant p8 as cache_control.replace
    participant p9 as _etag_matches
    participant p10 as if_none_match.split
    participant p11 as candidate.strip
    participant p12 as value.removeprefix
    participant p13 as request.headers.get
    participant p14 as Response
    p0->>p1: _resolve_payload
    p1-->>p2: action
    p1-->>p3: HTTPException
    p1-->>p3: HTTPException
    p0-->>p4: service.manifest_payload
    p0->>p5: _response
    p5->>p6: get_settings
    p6->>p7: Settings
    p5-->>p8: cache_control.replace
    p5->>p9: _etag_matches
    p9-->>p10: if_none_match.split
    p9-->>p11: candidate.strip
    p9-->>p12: value.removeprefix
    p5-->>p13: request.headers.get
    p5-->>p14: Response
    p5-->>p14: Response
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_agent_skill_bundle_manifest"]
    s2["2. _resolve_payload"]
    s3["3. action"]
    s4["4. HTTPException"]
    s5["5. HTTPException"]
    s6["6. service.manifest_payload"]
    s7["7. _response"]
    s8["8. get_settings"]
    s9["9. Settings"]
    s10["10. cache_control.replace"]
    s11["11. _etag_matches"]
    s12["12. if_none_match.split"]
    s1 -->|"_resolve_payload(...)"| s2
    s2 -. "action(data not statically known)" .-> s3
    s2 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Skill bundle resource not found.')" .-> s4
    s2 -. "HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Skill bundle artifacts are unavailable.')" .-> s5
    s1 -. "service.manifest_payload(skill_name, version)" .-> s6
    s1 -->|"_response(payload, request)"| s7
    s7 -->|"get_settings(data not statically known)"| s8
    s8 -->|"Settings(data not statically known)"| s9
    s7 -. "cache_control.replace('public,', 'private,', 1)" .-> s10
    s7 -->|"_etag_matches(request.headers.get(...), payload.etag)"| s11
    s11 -. "if_none_match.split(',')" .-> s12
    click s1 "../modules/agent_skill_bundles.md"
    click s2 "../modules/agent_skill_bundles.md"
    click s7 "../modules/agent_skill_bundles.md"
    click s8 "../modules/config.md"
    click s9 "../modules/config.md"
    click s11 "../modules/agent_skill_bundles.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_agent_skill_bundle_manifest` | `skill_name: str`, `version: str`, `request: Request`, `service: Annotated[AgentSkillBundleService, Depends(get_agent_skill_bundle_service)]`, `_access: Annotated[None, Depends(require_agent_skill_bundle_access)]` | - | - | `_response(...)` |
| `_resolve_payload` | `action: Callable[[], SkillBundlePayload]` | `SkillBundleNotFoundError`, `status`, `SkillBundleArtifactError`, `status` | - | `action(...)` |
| `action` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `service.manifest_payload` | - | - | - | - |
| `_response` | `payload: SkillBundlePayload`, `request: Request` | `status` | `headers[...]` | `Response(...)`, `Response(...)` |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `cache_control.replace` | - | - | - | - |
| `_etag_matches` | `if_none_match: str \| None`, `etag: str` | - | - | `False`, `True`, `False` |
| `if_none_match.split` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_agent_skill_bundle_manifest | _resolve_payload | 146 | `_resolve_payload(...)` |
| _resolve_payload | action | 67 | `action(data not statically known)` |
| _resolve_payload | HTTPException | 69 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Skill bundle resource not found.')` |
| _resolve_payload | HTTPException | 74 | `HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Skill bundle artifacts are unavailable.')` |
| get_agent_skill_bundle_manifest | service.manifest_payload | 146 | `service.manifest_payload(skill_name, version)` |
| get_agent_skill_bundle_manifest | _response | 147 | `_response(payload, request)` |
| _response | get_settings | 92 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| _response | cache_control.replace | 93 | `cache_control.replace('public,', 'private,', 1)` |
| _response | _etag_matches | 102 | `_etag_matches(request.headers.get(...), payload.etag)` |
| _etag_matches | if_none_match.split | 83 | `if_none_match.split(',')` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `_resolve_payload` | `action` | 67 |
| external_call | `_resolve_payload` | `HTTPException` | 69 |
| external_call | `_resolve_payload` | `HTTPException` | 74 |
| unresolved_call | `get_agent_skill_bundle_manifest` | `service.manifest_payload` | 146 |
| unresolved_call | `_response` | `cache_control.replace` | 93 |
| unresolved_call | `_etag_matches` | `if_none_match.split` | 83 |
| step_limit | `get_agent_skill_bundle_manifest` | `first 12 steps` | 0 |

## Behavior

This flow starts at `get_agent_skill_bundle_manifest` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
