# create_request_source_link

**Entry point:** `create_request_source_link` (`http`)
**Source:** [request_sources](../modules/request_sources.md)
**Modules touched:** [request_sources](../modules/request_sources.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_request_source_link
    participant p1 as RequestSourceLinkCreateRequest.model_validate
    participant p2 as service.create_link
    participant p3 as _bad_request
    participant p4 as _not_found
    participant p5 as HTTPException (backend/app/routers/reque…create_request_source_link)
    participant p6 as str (backend/app/routers/reque…create_request_source_link)
    participant p7 as HTTPException (backend/app/routers/request_sources.py:_bad_request)
    participant p8 as HTTPException (backend/app/routers/request_sources.py:_not_found)
    participant p9 as str (backend/app/routers/request_sources.py:_bad_request)
    participant p10 as str (backend/app/routers/request_sources.py:_not_found)
    p0-->>p1: RequestSourceLinkCreateRequest.model_validate(raw_data)
    p0-->>p2: service.create_link(data)
    p0->>p3: _bad_request
    p0->>p3: _bad_request
    p0->>p4: _not_found
    p0->>p4: _not_found
    p0-->>p5: HTTPException (backend/app/routers/reque…create_request_source_link)(status_code=status.HTTP_409_CONFLICT, detail=str(...))
    p0-->>p6: str (backend/app/routers/reque…create_request_source_link)(e)
    p3-->>p7: HTTPException (backend/app/routers/request_sources.py:_bad_request)(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))
    p4-->>p8: HTTPException (backend/app/routers/request_sources.py:_not_found)(status_code=status.HTTP_404_NOT_FOUND, detail=str(...))
    p3-->>p9: str (backend/app/routers/request_sources.py:_bad_request)(error)
    p4-->>p10: str (backend/app/routers/request_sources.py:_not_found)(error)
```

> Call sequence diagram shows 12 of 12 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 6 of 6 (0 omitted); unresolved 2 of 2 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 5; effect analysis evaluated: 5, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 5 source steps with known totals: observed: 21, emitted: 21, omitted: 0. Unavailable totals are excluded.

```mermaid
flowchart LR
    s1["1. create_request_source_link"]
    s2["2. RequestSourceLinkCreateRequest.model_validate"]
    s3["3. service.create_link"]
    s4["4. _bad_request"]
    s5["5. HTTPException (backend/app/routers/request_sources.py:_bad_request)"]
    s6["6. str (backend/app/routers/request_sources.py:_bad_request)"]
    s7["7. _bad_request"]
    s8["8. _not_found"]
    s9["9. HTTPException (backend/app/routers/request_sources.py:_not_found)"]
    s10["10. str (backend/app/routers/request_sources.py:_not_found)"]
    s11["11. _not_found"]
    s12["12. HTTPException (backend/app/routers/reque…create_request_source_link)"]
    s1 -. "RequestSourceLinkCreateRequest.model_validate(raw_data)" .-> s2
    s1 -. "service.create_link(data)" .-> s3
    s1 -->|"_bad_request(e)"| s4
    s4 -. "HTTPException (backend/app/routers/request_sources.py:_bad_request)(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s5
    s4 -. "str (backend/app/routers/request_sources.py:_bad_request)(error)" .-> s6
    s1 -->|"_bad_request(e)"| s7
    s1 -->|"_not_found(e)"| s8
    s8 -. "HTTPException (backend/app/routers/request_sources.py:_not_found)(status_code=status.HTTP_404_NOT_FOUND, detail=str(...))" .-> s9
    s8 -. "str (backend/app/routers/request_sources.py:_not_found)(error)" .-> s10
    s1 -->|"_not_found(e)"| s11
    s1 -. "HTTPException (backend/app/routers/reque…create_request_source_link)(status_code=status.HTTP_409_CONFLICT, detail=str(...))" .-> s12
    click s1 "../modules/request_sources.md"
    click s4 "../modules/request_sources.md"
    click s7 "../modules/request_sources.md"
    click s8 "../modules/request_sources.md"
    click s11 "../modules/request_sources.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_request_source_link` | `raw_data: Annotated[dict, Body(...)]`, `service: Annotated[RequestSourceService, Depends(get_request_source_service)]` | `ValidationError`, `RequestSourceValidationError`, `RequestSourceTargetNotFoundError`, `RequestSourceNotFoundError`, `RequestSourceConflictError`, `status` | - | `...` |
| `RequestSourceLinkCreateRequest.model_validate` | - | - | - | - |
| `service.create_link` | - | - | - | - |
| `_bad_request` | `error: Exception` | `status` | - | `HTTPException(...)` |
| `HTTPException (backend/app/routers/request_sources.py:_bad_request)` | - | - | - | - |
| `str (backend/app/routers/request_sources.py:_bad_request)` | - | - | - | - |
| `_bad_request` | `error: Exception` | `status` | - | `HTTPException(...)` |
| `_not_found` | `error: Exception` | `status` | - | `HTTPException(...)` |
| `HTTPException (backend/app/routers/request_sources.py:_not_found)` | - | - | - | - |
| `str (backend/app/routers/request_sources.py:_not_found)` | - | - | - | - |
| `_not_found` | `error: Exception` | `status` | - | `HTTPException(...)` |
| `HTTPException (backend/app/routers/reque…create_request_source_link)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_request_source_link | RequestSourceLinkCreateRequest.model_validate | 84 | `RequestSourceLinkCreateRequest.model_validate(raw_data)` |
| create_request_source_link | service.create_link | 85 | `service.create_link(data)` |
| create_request_source_link | _bad_request | 87 | `_bad_request(e)` |
| _bad_request | HTTPException (backend/app/routers/request_sources.py:_bad_request) | 34 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| _bad_request | str (backend/app/routers/request_sources.py:_bad_request) | 34 | `str(error)` |
| create_request_source_link | _bad_request | 89 | `_bad_request(e)` |
| create_request_source_link | _not_found | 91 | `_not_found(e)` |
| _not_found | HTTPException (backend/app/routers/request_sources.py:_not_found) | 38 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(...))` |
| _not_found | str (backend/app/routers/request_sources.py:_not_found) | 38 | `str(error)` |
| create_request_source_link | _not_found | 93 | `_not_found(e)` |
| create_request_source_link | HTTPException (backend/app/routers/reque…create_request_source_link) | 95 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `create_request_source_link` | `RequestSourceLinkCreateRequest.model_validate` | 84 |
| unresolved_call | `create_request_source_link` | `service.create_link` | 85 |
| external_call | `_bad_request` | `HTTPException` | 34 |
| external_call | `_not_found` | `HTTPException` | 38 |
| external_call | `create_request_source_link` | `HTTPException` | 95 |
| step_limit | `create_request_source_link` | `first 12 steps` | 0 |

## Behavior

This flow starts at `create_request_source_link` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
