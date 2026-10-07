# create_iteration

**Entry point:** `create_iteration` (`http`)
**Source:** [iterations](../modules/iterations.md)
**Modules touched:** [iterations](../modules/iterations.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_iteration
    participant p1 as service.create
    participant p2 as HTTPException
    participant p3 as str
    participant p4 as service.to_response
    p0-->>p1: service.create
    p0-->>p2: HTTPException
    p0-->>p3: str
    p0-->>p4: service.to_response
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. create_iteration"]
    s2["2. service.create"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. service.to_response"]
    s1 -. "service.create(data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str(e)" .-> s4
    s1 -. "service.to_response(iteration)" .-> s5
    click s1 "../modules/iterations.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_iteration` | `data: IterationCreate`, `service: Annotated[IterationService, Depends(get_iteration_service)]` | `status` | - | `service.to_response(...)` |
| `service.create` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `service.to_response` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_iteration | service.create | 80 | `service.create(data)` |
| create_iteration | HTTPException | 82 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| create_iteration | str | 84 | `str(e)` |
| create_iteration | service.to_response | 86 | `service.to_response(iteration)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `create_iteration` | `service.create` | 80 |
| external_call | `create_iteration` | `HTTPException` | 82 |
| unresolved_call | `create_iteration` | `service.to_response` | 86 |

## Behavior

This flow starts at `create_iteration` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
