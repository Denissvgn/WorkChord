# create_team_member_profile

**Entry point:** `create_team_member_profile` (`http`)
**Source:** [routers_team](../modules/routers_team.md)
**Modules touched:** [routers_team](../modules/routers_team.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_team_member_profile
    participant p1 as service.create_profile
    p0-->>p1: service.create_profile
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. create_team_member_profile"]
    s2["2. service.create_profile"]
    s1 -. "service.create_profile(data)" .-> s2
    click s1 "../modules/routers_team.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_team_member_profile` | `data: TeamMemberProfileCreate`, `service: Annotated[TeamService, Depends(get_team_service)]` | - | - | `...` |
| `service.create_profile` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_team_member_profile | service.create_profile | 75 | `service.create_profile(data)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `create_team_member_profile` | `service.create_profile` | 75 |

## Behavior

This flow starts at `create_team_member_profile` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
