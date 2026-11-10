# discover_agent_skill_bundles

**Entry point:** `discover_agent_skill_bundles` (`http`)
**Source:** [agent_skill_bundles](../modules/agent_skill_bundles.md)
**Modules touched:** [agent_skill_bundles](../modules/agent_skill_bundles.md), [config](../modules/config.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as discover_agent_skill_bundles
    participant p1 as get_settings().api_prefix.rstrip
    participant p2 as get_settings
    participant p3 as _resolve_payload
    participant p4 as service.discovery_payload
    participant p5 as _response
    participant p6 as Settings
    participant p7 as action
    participant p8 as HTTPException
    participant p9 as cache_control.replace
    participant p10 as _etag_matches
    participant p11 as request.headers.get
    participant p12 as Response
    participant p13 as if_none_match.split
    participant p14 as candidate.strip
    participant p15 as value.removeprefix
    p0-->>p1: get_settings().api_prefix.rstrip('/')
    p0->>p2: get_settings
    p0->>p3: _resolve_payload
    p0-->>p4: service.discovery_payload(...)
    p0->>p5: _response
    p2->>p6: Settings
    p3-->>p7: action
    p5->>p2: get_settings
    p3-->>p8: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Skill bundle resource not found.')
    p5-->>p9: cache_control.replace('public,', 'private,', 1)
    p3-->>p8: HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Skill bundle artifacts are unavailable.')
    p5->>p10: _etag_matches
    p5-->>p11: request.headers.get('if-none-match')
    p5-->>p12: Response(status_code=status.HTTP_304_NOT_MODIFIED, headers=headers)
    p5-->>p12: Response(content=payload.content, media_type=payload.media_type, headers=headers)
    p10-->>p13: if_none_match.split(',')
    p10-->>p14: candidate.strip
    p10-->>p15: value.removeprefix('W/')
```

> Call sequence diagram shows 18 of 18 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 4 of 4 (0 omitted); unresolved 8 of 8 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 7; effect analysis evaluated: 6, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 6 source steps with known totals: observed: 23, emitted: 23, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `discover_agent_skill_bundles` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `get_settings().api_prefix.rstrip` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `_resolve_payload` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `action` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `service.discovery_payload` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_response` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `cache_control.replace` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

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
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| discover_agent_skill_bundles | _resolve_payload | 118 | `_resolve_payload(...)` |
| _resolve_payload | action | 67 | `action(data not statically known)` |
| _resolve_payload | HTTPException | 69 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Skill bundle resource not found.')` |
| _resolve_payload | HTTPException | 74 | `HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Skill bundle artifacts are unavailable.')` |
| discover_agent_skill_bundles | service.discovery_payload | 119 | `service.discovery_payload(...)` |
| discover_agent_skill_bundles | _response | 121 | `_response(payload, request)` |
| _response | get_settings | 92 | `get_settings(data not statically known)` |
| _response | cache_control.replace | 93 | `cache_control.replace('public,', 'private,', 1)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

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
