# list_team_member_profiles

**Entry point:** `list_team_member_profiles` (`http`)
**Source:** [routers_team](../modules/routers_team.md)
**Modules touched:** [routers_team](../modules/routers_team.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_team_member_profiles
    participant p1 as service.list_profiles
    p0-->>p1: service.list_profiles
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. list_team_member_profiles"]
    s2["2. service.list_profiles"]
    s1 -. "service.list_profiles(data not statically known)" .-> s2
    click s1 "../modules/routers_team.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_team_member_profiles` | `service: Annotated[TeamService, Depends(get_team_service)]` | - | - | `...` |
| `service.list_profiles` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_team_member_profiles | service.list_profiles | 62 | `service.list_profiles(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_team_member_profiles` | `service.list_profiles` | 62 |

## Behavior

This flow starts at `list_team_member_profiles` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
