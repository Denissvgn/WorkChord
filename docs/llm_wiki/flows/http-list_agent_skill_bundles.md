# list_agent_skill_bundles

**Entry point:** `list_agent_skill_bundles` (`http`)
**Source:** [agent_skill_bundles](../modules/agent_skill_bundles.md)
**Modules touched:** [agent_skill_bundles](../modules/agent_skill_bundles.md), [config](../modules/config.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_agent_skill_bundles
    participant p1 as _response
    participant p2 as get_settings
    participant p3 as Settings
    participant p4 as cache_control.replace
    participant p5 as _etag_matches
    participant p6 as if_none_match.split
    participant p7 as candidate.strip
    participant p8 as value.removeprefix
    participant p9 as request.headers.get
    participant p10 as Response
    participant p11 as _resolve_payload
    participant p12 as action
    participant p13 as HTTPException
    p0->>p1: _response
    p1->>p2: get_settings
    p2->>p3: Settings
    p1-->>p4: cache_control.replace
    p1->>p5: _etag_matches
    p5-->>p6: if_none_match.split
    p5-->>p7: candidate.strip
    p5-->>p8: value.removeprefix
    p1-->>p9: request.headers.get
    p1-->>p10: Response
    p1-->>p10: Response
    p0->>p11: _resolve_payload
    p11-->>p12: action
    p11-->>p13: HTTPException
    p11-->>p13: HTTPException
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. list_agent_skill_bundles"]
    s2["2. _response"]
    s3["3. get_settings"]
    s4["4. Settings"]
    s5["5. cache_control.replace"]
    s6["6. _etag_matches"]
    s7["7. if_none_match.split"]
    s8["8. candidate.strip"]
    s9["9. value.removeprefix"]
    s10["10. request.headers.get"]
    s11["11. Response"]
    s12["12. Response"]
    s1 -->|"_response(_resolve_payload(...), request)"| s2
    s2 -->|"get_settings(data not statically known)"| s3
    s3 -->|"Settings(data not statically known)"| s4
    s2 -. "cache_control.replace('public,', 'private,', 1)" .-> s5
    s2 -->|"_etag_matches(request.headers.get(...), payload.etag)"| s6
    s6 -. "if_none_match.split(',')" .-> s7
    s6 -. "candidate.strip(data not statically known)" .-> s8
    s6 -. "value.removeprefix('W/')" .-> s9
    s2 -. "request.headers.get('if-none-match')" .-> s10
    s2 -. "Response(status_code=status.HTTP_304_NOT_MODIFIED, headers=headers)" .-> s11
    s2 -. "Response(content=payload.content, media_type=payload.media_type, headers=headers)" .-> s12
    click s1 "../modules/agent_skill_bundles.md"
    click s2 "../modules/agent_skill_bundles.md"
    click s3 "../modules/config.md"
    click s4 "../modules/config.md"
    click s6 "../modules/agent_skill_bundles.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_agent_skill_bundles` | `request: Request`, `service: Annotated[AgentSkillBundleService, Depends(get_agent_skill_bundle_service)]`, `_access: Annotated[None, Depends(require_agent_skill_bundle_access)]` | - | - | `_response(...)` |
| `_response` | `payload: SkillBundlePayload`, `request: Request` | `status` | `headers[...]` | `Response(...)`, `Response(...)` |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `cache_control.replace` | - | - | - | - |
| `_etag_matches` | `if_none_match: str \| None`, `etag: str` | - | - | `False`, `True`, `False` |
| `if_none_match.split` | - | - | - | - |
| `candidate.strip` | - | - | - | - |
| `value.removeprefix` | - | - | - | - |
| `request.headers.get` | - | - | - | - |
| `Response` | - | - | - | - |
| `Response` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_agent_skill_bundles | _response | 131 | `_response(_resolve_payload(...), request)` |
| _response | get_settings | 92 | `get_settings(data not statically known)` |
| get_settings | Settings | 479 | `Settings(data not statically known)` |
| _response | cache_control.replace | 93 | `cache_control.replace('public,', 'private,', 1)` |
| _response | _etag_matches | 102 | `_etag_matches(request.headers.get(...), payload.etag)` |
| _etag_matches | if_none_match.split | 83 | `if_none_match.split(',')` |
| _etag_matches | candidate.strip | 84 | `candidate.strip(data not statically known)` |
| _etag_matches | value.removeprefix | 85 | `value.removeprefix('W/')` |
| _response | request.headers.get | 102 | `request.headers.get('if-none-match')` |
| _response | Response | 103 | `Response(status_code=status.HTTP_304_NOT_MODIFIED, headers=headers)` |
| _response | Response | 104 | `Response(content=payload.content, media_type=payload.media_type, headers=headers)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `_response` | `cache_control.replace` | 93 |
| unresolved_call | `_etag_matches` | `if_none_match.split` | 83 |
| unresolved_call | `_etag_matches` | `candidate.strip` | 84 |
| unresolved_call | `_etag_matches` | `value.removeprefix` | 85 |
| unresolved_call | `_response` | `request.headers.get` | 102 |
| external_call | `_response` | `Response` | 103 |
| external_call | `_response` | `Response` | 104 |
| step_limit | `list_agent_skill_bundles` | `first 12 steps` | 0 |

## Behavior

This flow starts at `list_agent_skill_bundles` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
