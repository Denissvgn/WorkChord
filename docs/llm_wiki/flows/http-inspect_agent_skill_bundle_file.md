# inspect_agent_skill_bundle_file

**Entry point:** `inspect_agent_skill_bundle_file` (`http`)
**Source:** [agent_skill_bundles](../modules/agent_skill_bundles.md)
**Modules touched:** [agent_skill_bundles](../modules/agent_skill_bundles.md), [config](../modules/config.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as inspect_agent_skill_bundle_file
    participant p1 as _resolve_payload
    participant p2 as service.file_payload
    participant p3 as _response
    participant p4 as action
    participant p5 as get_settings
    participant p6 as HTTPException
    participant p7 as cache_control.replace
    participant p8 as _etag_matches
    participant p9 as request.headers.get
    participant p10 as Response
    participant p11 as Settings
    participant p12 as if_none_match.split
    participant p13 as candidate.strip
    participant p14 as value.removeprefix
    p0->>p1: _resolve_payload
    p0-->>p2: service.file_payload(skill_name, version, file_path)
    p0->>p3: _response
    p1-->>p4: action
    p3->>p5: get_settings
    p1-->>p6: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Skill bundle resource not found.')
    p3-->>p7: cache_control.replace('public,', 'private,', 1)
    p1-->>p6: HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Skill bundle artifacts are unavailable.')
    p3->>p8: _etag_matches
    p3-->>p9: request.headers.get('if-none-match')
    p3-->>p10: Response(status_code=status.HTTP_304_NOT_MODIFIED, headers=headers)
    p3-->>p10: Response(content=payload.content, media_type=payload.media_type, headers=headers)
    p5->>p11: Settings
    p8-->>p12: if_none_match.split(',')
    p8-->>p13: candidate.strip
    p8-->>p14: value.removeprefix('W/')
```

> Call sequence diagram shows 16 of 16 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 4 of 4 (0 omitted); unresolved 7 of 7 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 6; effect analysis evaluated: 5, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 5 source steps with known totals: observed: 25, emitted: 25, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `inspect_agent_skill_bundle_file` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `_resolve_payload` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `action` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `service.file_payload` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_response` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `cache_control.replace` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_etag_matches` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `if_none_match.split` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. inspect_agent_skill_bundle_file"]
    s2["2. _resolve_payload"]
    s3["3. action"]
    s4["4. HTTPException"]
    s5["5. HTTPException"]
    s6["6. service.file_payload"]
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
    s1 -. "service.file_payload(skill_name, version, file_path)" .-> s6
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
| `inspect_agent_skill_bundle_file` | `skill_name: str`, `version: str`, `file_path: str`, `request: Request`, `service: Annotated[AgentSkillBundleService, Depends(get_agent_skill_bundle_service)]`, `_access: Annotated[None, Depends(require_agent_skill_bundle_access)]` | - | - | `_response(...)` |
| `_resolve_payload` | `action: Callable[[], SkillBundlePayload]` | `SkillBundleNotFoundError`, `status`, `SkillBundleArtifactError`, `status` | - | `action(...)` |
| `action` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `service.file_payload` | - | - | - | - |
| `_response` | `payload: SkillBundlePayload`, `request: Request` | `status` | `headers[...]` | `Response(...)`, `Response(...)` |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `cache_control.replace` | - | - | - | - |
| `_etag_matches` | `if_none_match: str \| None`, `etag: str` | - | - | `False`, `True`, `False` |
| `if_none_match.split` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| inspect_agent_skill_bundle_file | _resolve_payload | 196 | `_resolve_payload(...)` |
| _resolve_payload | action | 67 | `action(data not statically known)` |
| _resolve_payload | HTTPException | 69 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Skill bundle resource not found.')` |
| _resolve_payload | HTTPException | 74 | `HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Skill bundle artifacts are unavailable.')` |
| inspect_agent_skill_bundle_file | service.file_payload | 197 | `service.file_payload(skill_name, version, file_path)` |
| inspect_agent_skill_bundle_file | _response | 199 | `_response(payload, request)` |
| _response | get_settings | 92 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| _response | cache_control.replace | 93 | `cache_control.replace('public,', 'private,', 1)` |
| _response | _etag_matches | 102 | `_etag_matches(request.headers.get(...), payload.etag)` |
| _etag_matches | if_none_match.split | 83 | `if_none_match.split(',')` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `_resolve_payload` | `action` | 67 |
| external_call | `_resolve_payload` | `HTTPException` | 69 |
| external_call | `_resolve_payload` | `HTTPException` | 74 |
| unresolved_call | `inspect_agent_skill_bundle_file` | `service.file_payload` | 197 |
| unresolved_call | `_response` | `cache_control.replace` | 93 |
| unresolved_call | `_etag_matches` | `if_none_match.split` | 83 |
| step_limit | `inspect_agent_skill_bundle_file` | `first 12 steps` | 0 |

## Behavior

This flow starts at `inspect_agent_skill_bundle_file` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
