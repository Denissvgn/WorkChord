# create_team_member

**Entry point:** `create_team_member` (`http`)
**Source:** [routers_team](../modules/routers_team.md)
**Modules touched:** [routers_team](../modules/routers_team.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_team_member
    participant p1 as service.create
    participant p2 as HTTPException
    participant p3 as str
    participant p4 as service.get_by_id
    p0-->>p1: service.create
    p0-->>p2: HTTPException
    p0-->>p3: str
    p0-->>p4: service.get_by_id
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. create_team_member"]
    s2["2. service.create"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. service.get_by_id"]
    s1 -. "service.create(iteration_id, data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str(e)" .-> s4
    s1 -. "service.get_by_id(member.id)" .-> s5
    click s1 "../modules/routers_team.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_team_member` | `iteration_id: int`, `data: TeamMemberCreate`, `service: Annotated[TeamService, Depends(get_team_service)]` | `status` | - | `...` |
| `service.create` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `service.get_by_id` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_team_member | service.create | 195 | `service.create(iteration_id, data)` |
| create_team_member | HTTPException | 197 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| create_team_member | str | 199 | `str(e)` |
| create_team_member | service.get_by_id | 201 | `service.get_by_id(member.id)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `create_team_member` | `service.create` | 195 |
| external_call | `create_team_member` | `HTTPException` | 197 |
| unresolved_call | `create_team_member` | `service.get_by_id` | 201 |

## Behavior

This flow starts at `create_team_member` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
