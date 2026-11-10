# list_request_source_links

**Entry point:** `list_request_source_links` (`http`)
**Source:** [request_sources](../modules/request_sources.md)
**Modules touched:** [request_sources](../modules/request_sources.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_request_source_links
    participant p1 as service.list_links_for_target
    participant p2 as _bad_request
    participant p3 as _not_found
    participant p4 as HTTPException (backend/app/routers/request_sources.py:_bad_request)
    participant p5 as HTTPException (backend/app/routers/request_sources.py:_not_found)
    participant p6 as str (backend/app/routers/request_sources.py:_bad_request)
    participant p7 as str (backend/app/routers/request_sources.py:_not_found)
    p0-->>p1: service.list_links_for_target(target_type, target_id)
    p0->>p2: _bad_request
    p0->>p3: _not_found
    p2-->>p4: HTTPException (backend/app/routers/request_sources.py:_bad_request)(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))
    p3-->>p5: HTTPException (backend/app/routers/request_sources.py:_not_found)(status_code=status.HTTP_404_NOT_FOUND, detail=str(...))
    p2-->>p6: str (backend/app/routers/request_sources.py:_bad_request)(error)
    p3-->>p7: str (backend/app/routers/request_sources.py:_not_found)(error)
```

> Call sequence diagram shows 7 of 7 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 4 of 4 (0 omitted); unresolved 1 of 1 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 3; effect analysis evaluated: 3, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 3 source steps with known totals: observed: 12, emitted: 12, omitted: 0. Unavailable totals are excluded.

```mermaid
flowchart LR
    s1["1. list_request_source_links"]
    s2["2. service.list_links_for_target"]
    s3["3. _bad_request"]
    s4["4. HTTPException (backend/app/routers/request_sources.py:_bad_request)"]
    s5["5. str (backend/app/routers/request_sources.py:_bad_request)"]
    s6["6. _not_found"]
    s7["7. HTTPException (backend/app/routers/request_sources.py:_not_found)"]
    s8["8. str (backend/app/routers/request_sources.py:_not_found)"]
    s1 -. "service.list_links_for_target(target_type, target_id)" .-> s2
    s1 -->|"_bad_request(e)"| s3
    s3 -. "HTTPException (backend/app/routers/request_sources.py:_bad_request)(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s4
    s3 -. "str (backend/app/routers/request_sources.py:_bad_request)(error)" .-> s5
    s1 -->|"_not_found(e)"| s6
    s6 -. "HTTPException (backend/app/routers/request_sources.py:_not_found)(status_code=status.HTTP_404_NOT_FOUND, detail=str(...))" .-> s7
    s6 -. "str (backend/app/routers/request_sources.py:_not_found)(error)" .-> s8
    click s1 "../modules/request_sources.md"
    click s3 "../modules/request_sources.md"
    click s6 "../modules/request_sources.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_request_source_links` | `service: Annotated[RequestSourceService, Depends(get_request_source_service)]`, `target_type: str`, `target_id: int` | `RequestSourceValidationError`, `RequestSourceTargetNotFoundError` | - | `...` |
| `service.list_links_for_target` | - | - | - | - |
| `_bad_request` | `error: Exception` | `status` | - | `HTTPException(...)` |
| `HTTPException (backend/app/routers/request_sources.py:_bad_request)` | - | - | - | - |
| `str (backend/app/routers/request_sources.py:_bad_request)` | - | - | - | - |
| `_not_found` | `error: Exception` | `status` | - | `HTTPException(...)` |
| `HTTPException (backend/app/routers/request_sources.py:_not_found)` | - | - | - | - |
| `str (backend/app/routers/request_sources.py:_not_found)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_request_source_links | service.list_links_for_target | 66 | `service.list_links_for_target(target_type, target_id)` |
| list_request_source_links | _bad_request | 68 | `_bad_request(e)` |
| _bad_request | HTTPException (backend/app/routers/request_sources.py:_bad_request) | 34 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| _bad_request | str (backend/app/routers/request_sources.py:_bad_request) | 34 | `str(error)` |
| list_request_source_links | _not_found | 70 | `_not_found(e)` |
| _not_found | HTTPException (backend/app/routers/request_sources.py:_not_found) | 38 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(...))` |
| _not_found | str (backend/app/routers/request_sources.py:_not_found) | 38 | `str(error)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_request_source_links` | `service.list_links_for_target` | 66 |
| external_call | `_bad_request` | `HTTPException` | 34 |
| external_call | `_not_found` | `HTTPException` | 38 |

## Behavior

This flow starts at `list_request_source_links` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
