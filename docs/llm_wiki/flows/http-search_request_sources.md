# search_request_sources

**Entry point:** `search_request_sources` (`http`)
**Source:** [request_sources](../modules/request_sources.md)
**Modules touched:** [request_sources](../modules/request_sources.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as search_request_sources
    participant p1 as service.search_sources
    participant p2 as _bad_request
    participant p3 as HTTPException
    participant p4 as str
    p0-->>p1: service.search_sources
    p0->>p2: _bad_request
    p2-->>p3: HTTPException
    p2-->>p4: str
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. search_request_sources"]
    s2["2. service.search_sources"]
    s3["3. _bad_request"]
    s4["4. HTTPException"]
    s5["5. str"]
    s1 -. "service.search_sources(q=q, source_type=source_type, limit=limit)" .-> s2
    s1 -->|"_bad_request(e)"| s3
    s3 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s4
    s3 -. "str(error)" .-> s5
    click s1 "../modules/request_sources.md"
    click s3 "../modules/request_sources.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `search_request_sources` | `service: Annotated[RequestSourceService, Depends(get_request_source_service)]`, `q: Optional[str]`, `source_type: Optional[str]`, `limit: int` | `RequestSourceValidationError` | - | `...` |
| `service.search_sources` | - | - | - | - |
| `_bad_request` | `error: Exception` | `status` | - | `HTTPException(...)` |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| search_request_sources | service.search_sources | 50 | `service.search_sources(q=q, source_type=source_type, limit=limit)` |
| search_request_sources | _bad_request | 52 | `_bad_request(e)` |
| _bad_request | HTTPException | 34 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| _bad_request | str | 34 | `str(error)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `search_request_sources` | `service.search_sources` | 50 |
| external_call | `_bad_request` | `HTTPException` | 34 |

## Behavior

This flow starts at `search_request_sources` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
