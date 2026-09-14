# get_team_members

**Entry point:** `get_team_members` (`http`)
**Source:** [routers_team](../modules/routers_team.md)
**Modules touched:** [routers_team](../modules/routers_team.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_team_members
    participant p1 as service.get_by_iteration
    p0-->>p1: service.get_by_iteration
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_team_members"]
    s2["2. service.get_by_iteration"]
    s1 -. "service.get_by_iteration(iteration_id)" .-> s2
    click s1 "../modules/routers_team.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_team_members` | `iteration_id: int`, `service: Annotated[TeamService, Depends(get_team_service)]` | - | - | `...` |
| `service.get_by_iteration` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_team_members | service.get_by_iteration | 38 | `service.get_by_iteration(iteration_id)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_team_members` | `service.get_by_iteration` | 38 |

## Behavior

This flow starts at `get_team_members` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
