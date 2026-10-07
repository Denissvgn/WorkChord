# get_iteration_planning_readiness

**Entry point:** `get_iteration_planning_readiness` (`http`)
**Source:** [iterations](../modules/iterations.md)
**Modules touched:** [iterations](../modules/iterations.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_iteration_planning_readiness
    participant p1 as service.get_planning_readiness_summary
    participant p2 as HTTPException
    p0-->>p1: service.get_planning_readiness_summary
    p0-->>p2: HTTPException
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_iteration_planning_readiness"]
    s2["2. service.get_planning_readiness_summary"]
    s3["3. HTTPException"]
    s1 -. "service.get_planning_readiness_summary(iteration_id)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    click s1 "../modules/iterations.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_iteration_planning_readiness` | `iteration_id: int`, `service: Annotated[IterationService, Depends(get_iteration_service)]` | `status` | - | `summary` |
| `service.get_planning_readiness_summary` | - | - | - | - |
| `HTTPException` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_iteration_planning_readiness | service.get_planning_readiness_summary | 187 | `service.get_planning_readiness_summary(iteration_id)` |
| get_iteration_planning_readiness | HTTPException | 189 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_iteration_planning_readiness` | `service.get_planning_readiness_summary` | 187 |
| external_call | `get_iteration_planning_readiness` | `HTTPException` | 189 |

## Behavior

This flow starts at `get_iteration_planning_readiness` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
