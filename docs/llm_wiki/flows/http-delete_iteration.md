# delete_iteration

**Entry point:** `delete_iteration` (`http`)
**Source:** [iterations](../modules/iterations.md)
**Modules touched:** [iterations](../modules/iterations.md), [schemas_common](../modules/schemas_common.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as delete_iteration
    participant p1 as service.delete
    participant p2 as HTTPException
    participant p3 as MessageResponse
    p0-->>p1: service.delete
    p0-->>p2: HTTPException
    p0->>p3: MessageResponse
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. delete_iteration"]
    s2["2. service.delete"]
    s3["3. HTTPException"]
    s4["4. MessageResponse"]
    s1 -. "service.delete(iteration_id)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    s1 -->|"MessageResponse(message=..., success=True)"| s4
    click s1 "../modules/iterations.md"
    click s4 "../modules/schemas_common.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `delete_iteration` | `iteration_id: int`, `service: Annotated[IterationService, Depends(get_iteration_service)]` | `status` | - | `MessageResponse(...)` |
| `service.delete` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `MessageResponse` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| delete_iteration | service.delete | 145 | `service.delete(iteration_id)` |
| delete_iteration | HTTPException | 147 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| delete_iteration | MessageResponse | 151 | `MessageResponse(message=..., success=True)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `delete_iteration` | `service.delete` | 145 |
| external_call | `delete_iteration` | `HTTPException` | 147 |

## Behavior

This flow starts at `delete_iteration` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
