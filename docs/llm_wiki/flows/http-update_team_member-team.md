# update_team_member

**Entry point:** `update_team_member` (`http`)
**Source:** [routers_team](../modules/routers_team.md)
**Modules touched:** [routers_team](../modules/routers_team.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_team_member
    participant p1 as service.update
    participant p2 as HTTPException
    participant p3 as str
    p0-->>p1: service.update
    p0-->>p2: HTTPException
    p0-->>p3: str
    p0-->>p2: HTTPException
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. update_team_member"]
    s2["2. service.update"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. HTTPException"]
    s1 -. "service.update(member_id, data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str(e)" .-> s4
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s5
    b0["mutation service.update"]
    s1 -. "mutation service.update" .-> b0
    click s1 "../modules/routers_team.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `update_team_member` | `member_id: int`, `data: TeamMemberUpdate`, `service: Annotated[TeamService, Depends(get_team_service)]` | `status`, `status` | - | `member` |
| `service.update` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| update_team_member | service.update | 227 | `service.update(member_id, data)` |
| update_team_member | HTTPException | 229 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| update_team_member | str | 231 | `str(e)` |
| update_team_member | HTTPException | 234 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `service.update` | `update_team_member` | 227 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `update_team_member` | `HTTPException` | 229 |
| external_call | `update_team_member` | `HTTPException` | 234 |

## Behavior

This flow starts at `update_team_member` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
