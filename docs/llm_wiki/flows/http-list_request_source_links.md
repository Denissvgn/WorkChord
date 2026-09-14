# list_request_source_links

**Entry point:** `list_request_source_links` (`http`)
**Source:** [request_sources](../modules/request_sources.md)
**Modules touched:** [request_sources](../modules/request_sources.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_request_source_links
    participant p1 as service.list_links_for_target
    participant p2 as _bad_request
    participant p3 as HTTPException (backend/app/routers/request_sources.py:_bad_request)
    participant p4 as str (backend/app/routers/request_sources.py:_bad_request)
    participant p5 as _not_found
    participant p6 as HTTPException (backend/app/routers/request_sources.py:_not_found)
    participant p7 as str (backend/app/routers/request_sources.py:_not_found)
    p0-->>p1: service.list_links_for_target
    p0->>p2: _bad_request
    p2-->>p3: HTTPException (backend/app/routers/request_sources.py:_bad_request)
    p2-->>p4: str (backend/app/routers/request_sources.py:_bad_request)
    p0->>p5: _not_found
    p5-->>p6: HTTPException (backend/app/routers/request_sources.py:_not_found)
    p5-->>p7: str (backend/app/routers/request_sources.py:_not_found)
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_request_source_links` | `service.list_links_for_target` | 66 |
| external_call | `_bad_request` | `HTTPException` | 34 |
| external_call | `_not_found` | `HTTPException` | 38 |

## Behavior

This flow starts at `list_request_source_links` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
