# get_my_agent_work

**Entry point:** `get_my_agent_work` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [routers_agent](../modules/routers_agent.md), [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_my_agent_work
    participant p1 as _if_none_match_matches
    participant p2 as _handle_agent_error
    participant p3 as utc_now
    participant p4 as _if_none_match_matches.<locals>.normalize
    participant p5 as max
    participant p6 as service.get_work
    participant p7 as service.work_etag
    participant p8 as int
    participant p9 as (…).total_seconds
    participant p10 as str (backend/app/routers/agent.py:get_my_agent_work)
    participant p11 as Response
    participant p12 as response.headers.update
    participant p13 as isinstance
    participant p14 as datetime.now
    participant p15 as str (backend/app/routers/agent.py:_handle_agent_error)
    participant p16 as any
    participant p17 as candidate.strip
    participant p18 as HTTPException
    participant p19 as value.split
    participant p20 as exc.detail
    p0->>p1: _if_none_match_matches
    p0->>p2: _handle_agent_error
    p0->>p3: utc_now
    p1->>p4: _if_none_match_matches.<locals>.normalize
    p0-->>p5: max(1, int(...))
    p0-->>p6: service.get_work(actor, limit=limit, cursor=cursor)
    p0-->>p7: service.work_etag(decision, cursor=cursor, limit=limit)
    p0-->>p8: int(...)
    p0-->>p9: (…).total_seconds
    p0-->>p10: str (backend/app/routers/agent.py:get_my_agent_work)(retry_after)
    p0-->>p11: Response(status_code=status.HTTP_304_NOT_MODIFIED, headers=cache_headers)
    p0-->>p12: response.headers.update(cache_headers)
    p2-->>p13: isinstance(exc, AgentPermissionError)
    p3-->>p14: datetime.now(UTC)
    p2-->>p15: str (backend/app/routers/agent.py:_handle_agent_error)(exc)
    p1-->>p16: any(...)
    p2-->>p15: str (backend/app/routers/agent.py:_handle_agent_error)(exc)
    p1-->>p17: candidate.strip
    p2-->>p18: HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
    p2-->>p13: isinstance(exc, AgentRoutingConflictError)
    p1-->>p19: value.split(',')
    p2-->>p18: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p20: exc.detail
    p2-->>p13: isinstance(exc, AgentTeamSetupConflictError)
    p2-->>p18: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p20: exc.detail
    p2-->>p13: isinstance(exc, TaskVersionConflictError)
    p2-->>p18: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p20: exc.detail
    p2-->>p13: isinstance(exc, AgentConflictError)
```

> Call sequence diagram shows 30 of 44 interactions; 14 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 17 of 28 (11 omitted); unresolved 9 of 11 (2 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/routers/agent.py:_handle_agent_error` | 3 | - | external | 11 |
| `backend/app/routers/agent.py:_if_none_match_matches.<locals>.normalize` | 37 | - | unresolved | 2 |
| `backend/app/routers/agent.py:_if_none_match_matches` | 36 | [backend/app/routers/agent.py](../modules/routers_agent.md) | internal | 1 |
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 6; effect analysis evaluated: 5, partial: 1, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 6 source steps with known totals: observed: 35, emitted: 31, omitted: 4. Unavailable totals are excluded.

- Effect collector omitted observations before flow assembly; displayed effects are partial.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `get_my_agent_work` | `available` | `evaluated` | `available` | `11` | `11` | `0` |
| `service.get_work` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_handle_agent_error` | `available` | `partial` | `available` | `14` | `10` | `4` |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/routers/agent.py:_handle_agent_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/routers/agent.py:_handle_agent_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. get_my_agent_work"]
    s2["2. service.get_work"]
    s3["3. _handle_agent_error"]
    s4["4. isinstance"]
    s5["5. str (backend/app/routers/agent.py:_handle_agent_error)"]
    s6["6. str (backend/app/routers/agent.py:_handle_agent_error)"]
    s7["7. HTTPException"]
    s8["8. isinstance"]
    s9["9. HTTPException"]
    s10["10. exc.detail"]
    s11["11. isinstance"]
    s12["12. HTTPException"]
    s1 -. "service.get_work(actor, limit=limit, cursor=cursor)" .-> s2
    s1 -->|"_handle_agent_error(exc, structured=True)"| s3
    s3 -. "isinstance(exc, AgentPermissionError)" .-> s4
    s3 -. "str (backend/app/routers/agent.py:_handle_agent_error)(exc)" .-> s5
    s3 -. "str (backend/app/routers/agent.py:_handle_agent_error)(exc)" .-> s6
    s3 -. "HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)" .-> s7
    s3 -. "isinstance(exc, AgentRoutingConflictError)" .-> s8
    s3 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s9
    s3 -. "exc.detail(data not statically known)" .-> s10
    s3 -. "isinstance(exc, AgentTeamSetupConflictError)" .-> s11
    s3 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s12
    b0["mutation response.headers.update"]
    s1 -. "mutation response.headers.update" .-> b0
    click s1 "../modules/routers_agent.md"
    click s3 "../modules/routers_agent.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_my_agent_work` | `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `service: Annotated[AgentWorkService, Depends(get_agent_work_service)]`, `response: Response`, `limit: int`, `cursor: Optional[str]`, `if_none_match: Annotated[Optional[str], Header(alias='If-None-Match')]` | `status` | `cache_headers[...]` | `Response(...)`, `decision` |
| `service.get_work` | - | - | - | - |
| `_handle_agent_error` | `exc: Exception`, `structured: bool` | `AgentPermissionError`, `status`, `AgentRoutingConflictError`, `status`, `AgentTeamSetupConflictError`, `status`, `TaskVersionConflictError`, `status` | - | - |
| `isinstance` | - | - | - | - |
| `str (backend/app/routers/agent.py:_handle_agent_error)` | - | - | - | - |
| `str (backend/app/routers/agent.py:_handle_agent_error)` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_my_agent_work | service.get_work | 781 | `service.get_work(actor, limit=limit, cursor=cursor)` |
| get_my_agent_work | _handle_agent_error | 783 | `_handle_agent_error(exc, structured=True)` |
| _handle_agent_error | isinstance | 254 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | str (backend/app/routers/agent.py:_handle_agent_error) | 256 | `str(exc)` |
| _handle_agent_error | str (backend/app/routers/agent.py:_handle_agent_error) | 258 | `str(exc)` |
| _handle_agent_error | HTTPException | 260 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)` |
| _handle_agent_error | isinstance | 261 | `isinstance(exc, AgentRoutingConflictError)` |
| _handle_agent_error | HTTPException | 262 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 262 | `exc.detail(data not statically known)` |
| _handle_agent_error | isinstance | 263 | `isinstance(exc, AgentTeamSetupConflictError)` |
| _handle_agent_error | HTTPException | 264 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `response.headers.update` | `get_my_agent_work` | 798 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_my_agent_work` | `service.get_work` | 781 |
| external_call | `_handle_agent_error` | `isinstance` | 254 |
| external_call | `_handle_agent_error` | `HTTPException` | 260 |
| external_call | `_handle_agent_error` | `isinstance` | 261 |
| external_call | `_handle_agent_error` | `HTTPException` | 262 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 262 |
| external_call | `_handle_agent_error` | `isinstance` | 263 |
| external_call | `_handle_agent_error` | `HTTPException` | 264 |
| step_limit | `get_my_agent_work` | `first 12 steps` | 0 |

## Behavior

This flow starts at `get_my_agent_work` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
