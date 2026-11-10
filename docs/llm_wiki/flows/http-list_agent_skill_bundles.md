# list_agent_skill_bundles

**Entry point:** `list_agent_skill_bundles` (`http`)
**Source:** [agent_skill_bundles](../modules/agent_skill_bundles.md)
**Modules touched:** [agent_skill_bundles](../modules/agent_skill_bundles.md), [config](../modules/config.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_agent_skill_bundles
    participant p1 as _response
    participant p2 as _resolve_payload
    participant p3 as get_settings
    participant p4 as action
    participant p5 as cache_control.replace
    participant p6 as HTTPException
    participant p7 as _etag_matches
    participant p8 as request.headers.get
    participant p9 as Response
    participant p10 as Settings
    participant p11 as if_none_match.split
    participant p12 as candidate.strip
    participant p13 as value.removeprefix
    p0->>p1: _response
    p0->>p2: _resolve_payload
    p1->>p3: get_settings
    p2-->>p4: action
    p1-->>p5: cache_control.replace('public,', 'private,', 1)
    p2-->>p6: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Skill bundle resource not found.')
    p1->>p7: _etag_matches
    p2-->>p6: HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Skill bundle artifacts are unavailable.')
    p1-->>p8: request.headers.get('if-none-match')
    p1-->>p9: Response(status_code=status.HTTP_304_NOT_MODIFIED, headers=headers)
    p1-->>p9: Response(content=payload.content, media_type=payload.media_type, headers=headers)
    p3->>p10: Settings
    p7-->>p11: if_none_match.split(',')
    p7-->>p12: candidate.strip
    p7-->>p13: value.removeprefix('W/')
```

> Call sequence diagram shows 15 of 15 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 4 of 4 (0 omitted); unresolved 6 of 6 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 6; effect analysis evaluated: 5, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 5 source steps with known totals: observed: 22, emitted: 22, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `list_agent_skill_bundles` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `_response` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `cache_control.replace` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_etag_matches` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `if_none_match.split` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `candidate.strip` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `value.removeprefix` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `request.headers.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `Response` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `Response` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

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
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| _response | cache_control.replace | 93 | `cache_control.replace('public,', 'private,', 1)` |
| _response | _etag_matches | 102 | `_etag_matches(request.headers.get(...), payload.etag)` |
| _etag_matches | if_none_match.split | 83 | `if_none_match.split(',')` |
| _etag_matches | candidate.strip | 84 | `candidate.strip(data not statically known)` |
| _etag_matches | value.removeprefix | 85 | `value.removeprefix('W/')` |
| _response | request.headers.get | 102 | `request.headers.get('if-none-match')` |
| _response | Response | 103 | `Response(status_code=status.HTTP_304_NOT_MODIFIED, headers=headers)` |
| _response | Response | 104 | `Response(content=payload.content, media_type=payload.media_type, headers=headers)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

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
