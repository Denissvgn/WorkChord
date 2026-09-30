# get_team_member

**Entry point:** `get_team_member` (`http`)
**Source:** [routers_team](../modules/routers_team.md)
**Modules touched:** [routers_team](../modules/routers_team.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_team_member
    participant p1 as service.get_by_id
    participant p2 as HTTPException
    p0-->>p1: service.get_by_id
    p0-->>p2: HTTPException
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_team_member"]
    s2["2. service.get_by_id"]
    s3["3. HTTPException"]
    s1 -. "service.get_by_id(member_id)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    click s1 "../modules/routers_team.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_team_member` | `member_id: int`, `service: Annotated[TeamService, Depends(get_team_service)]` | `status` | - | `member` |
| `service.get_by_id` | - | - | - | - |
| `HTTPException` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_team_member | service.get_by_id | 210 | `service.get_by_id(member_id)` |
| get_team_member | HTTPException | 212 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_team_member` | `service.get_by_id` | 210 |
| external_call | `get_team_member` | `HTTPException` | 212 |

## Behavior

This flow starts at `get_team_member` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
