# get_iterations

**Entry point:** `get_iterations` (`http`)
**Source:** [iterations](../modules/iterations.md)
**Modules touched:** [iterations](../modules/iterations.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_iterations
    participant p1 as ValueError
    participant p2 as service.get_all
    participant p3 as service.get_page
    participant p4 as HTTPException
    participant p5 as str
    participant p6 as service.to_response
    p0-->>p1: ValueError
    p0-->>p2: service.get_all
    p0-->>p3: service.get_page
    p0-->>p4: HTTPException
    p0-->>p5: str
    p0-->>p6: service.to_response
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_iterations"]
    s2["2. ValueError"]
    s3["3. service.get_all"]
    s4["4. service.get_page"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. service.to_response"]
    s1 -. "ValueError('an iteration cursor requires an explicit limit')" .-> s2
    s1 -. "service.get_all(data not statically known)" .-> s3
    s1 -. "service.get_page(limit=limit, cursor_start_date=cursor_start_date, cursor_id=cursor_id)" .-> s4
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s5
    s1 -. "str(exc)" .-> s6
    s1 -. "service.to_response(iteration)" .-> s7
    click s1 "../modules/iterations.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_iterations` | `service: Annotated[IterationService, Depends(get_iteration_service)]`, `limit: Annotated[int \| None, Query(ge=1, le=MAX_ITERATION_LIST_ITEMS)]`, `cursor_start_date: date \| None`, `cursor_id: int \| None` | `status` | - | `...` |
| `ValueError` | - | - | - | - |
| `service.get_all` | - | - | - | - |
| `service.get_page` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `service.to_response` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_iterations | ValueError | 53 | `ValueError('an iteration cursor requires an explicit limit')` |
| get_iterations | service.get_all | 54 | `service.get_all(data not statically known)` |
| get_iterations | service.get_page | 56 | `service.get_page(limit=limit, cursor_start_date=cursor_start_date, cursor_id=cursor_id)` |
| get_iterations | HTTPException | 62 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| get_iterations | str | 64 | `str(exc)` |
| get_iterations | service.to_response | 66 | `service.to_response(iteration)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `get_iterations` | `ValueError` | 53 |
| unresolved_call | `get_iterations` | `service.get_all` | 54 |
| unresolved_call | `get_iterations` | `service.get_page` | 56 |
| external_call | `get_iterations` | `HTTPException` | 62 |
| unresolved_call | `get_iterations` | `service.to_response` | 66 |

## Behavior

This flow starts at `get_iterations` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
