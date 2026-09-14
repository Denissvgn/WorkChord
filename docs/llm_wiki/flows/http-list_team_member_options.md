# list_team_member_options

**Entry point:** `list_team_member_options` (`http`)
**Source:** [routers_team](../modules/routers_team.md)
**Modules touched:** [routers_team](../modules/routers_team.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_team_member_options
    participant p1 as service.list_member_options
    p0-->>p1: service.list_member_options
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. list_team_member_options"]
    s2["2. service.list_member_options"]
    s1 -. "service.list_member_options(data not statically known)" .-> s2
    click s1 "../modules/routers_team.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_team_member_options` | `service: Annotated[TeamService, Depends(get_team_service)]` | - | - | `...` |
| `service.list_member_options` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_team_member_options | service.list_member_options | 54 | `service.list_member_options(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_team_member_options` | `service.list_member_options` | 54 |

## Behavior

This flow starts at `list_team_member_options` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
