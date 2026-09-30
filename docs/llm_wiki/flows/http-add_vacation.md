# add_vacation

**Entry point:** `add_vacation` (`http`)
**Source:** [routers_team](../modules/routers_team.md)
**Modules touched:** [routers_team](../modules/routers_team.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as add_vacation
    participant p1 as service.add_vacation
    participant p2 as HTTPException
    p0-->>p1: service.add_vacation
    p0-->>p2: HTTPException
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. add_vacation"]
    s2["2. service.add_vacation"]
    s3["3. HTTPException"]
    s1 -. "service.add_vacation(member_id, data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    click s1 "../modules/routers_team.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `add_vacation` | `member_id: int`, `data: VacationCreate`, `service: Annotated[TeamService, Depends(get_team_service)]` | `status` | - | `vacation` |
| `service.add_vacation` | - | - | - | - |
| `HTTPException` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| add_vacation | service.add_vacation | 315 | `service.add_vacation(member_id, data)` |
| add_vacation | HTTPException | 317 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `add_vacation` | `service.add_vacation` | 315 |
| external_call | `add_vacation` | `HTTPException` | 317 |

## Behavior

This flow starts at `add_vacation` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
