# get_member_workload

**Entry point:** `get_member_workload` (`http`)
**Source:** [routers_team](../modules/routers_team.md)
**Modules touched:** [routers_team](../modules/routers_team.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_member_workload
    participant p1 as service.get_workload
    participant p2 as HTTPException
    p0-->>p1: service.get_workload
    p0-->>p2: HTTPException
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_member_workload"]
    s2["2. service.get_workload"]
    s3["3. HTTPException"]
    s1 -. "service.get_workload(member_id)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    click s1 "../modules/routers_team.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_member_workload` | `member_id: int`, `service: Annotated[TeamService, Depends(get_team_service)]` | `status` | - | `workload` |
| `service.get_workload` | - | - | - | - |
| `HTTPException` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_member_workload | service.get_workload | 277 | `service.get_workload(member_id)` |
| get_member_workload | HTTPException | 279 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_member_workload` | `service.get_workload` | 277 |
| external_call | `get_member_workload` | `HTTPException` | 279 |

## Behavior

This flow starts at `get_member_workload` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
